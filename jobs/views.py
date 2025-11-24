import re
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from .models import Job, JobApplication, PipelineStage, ApplicationPipeline, SavedSearch, SearchNotification
from .forms import JobPostForm
from accounts.models import Profile, Message
from django.contrib.auth import get_user_model

User = get_user_model()


def _get_coordinates_from_location(location_text):
    """
    Get approximate coordinates for a location.
    This is a simplified version - in production, you'd use a geocoding API.
    Returns (latitude, longitude) tuple or (None, None) if not found.
    """
    # Common US cities coordinates (add more as needed)
    city_coordinates = {
        'atlanta': (33.7490, -84.3880),
        'atlanta, ga': (33.7490, -84.3880),
        'new york': (40.7128, -74.0060),
        'new york, ny': (40.7128, -74.0060),
        'los angeles': (34.0522, -118.2437),
        'los angeles, ca': (34.0522, -118.2437),
        'chicago': (41.8781, -87.6298),
        'chicago, il': (41.8781, -87.6298),
        'san francisco': (37.7749, -122.4194),
        'san francisco, ca': (37.7749, -122.4194),
        'boston': (42.3601, -71.0589),
        'boston, ma': (42.3601, -71.0589),
        'seattle': (47.6062, -122.3321),
        'seattle, wa': (47.6062, -122.3321),
        'austin': (30.2672, -97.7431),
        'austin, tx': (30.2672, -97.7431),
        'denver': (39.7392, -104.9903),
        'denver, co': (39.7392, -104.9903),
        'miami': (25.7617, -80.1918),
        'miami, fl': (25.7617, -80.1918),
    }
    
    location_lower = location_text.lower().strip()
    return city_coordinates.get(location_lower, (None, None))


def _calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    if None in (lat1, lon1, lat2, lon2):
        return None
    
    # Radius of Earth in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def _skill_tokens(text: str):
    if not text:
        return []
    # split on commas/newlines and non-alphanumerics; lower-case; dedupe
    raw = re.split(r"[,\n]+", text)
    tokens = []
    for chunk in raw:
        for t in re.findall(r"[A-Za-z0-9+#\.]+", chunk.lower()):
            if len(t) >= 2:
                tokens.append(t)
    return list(dict.fromkeys(tokens))  # preserve order, remove dups

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using Haversine formula"""
    if not all([lat1, lon1, lat2, lon2]):
        return float('inf')
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

@login_required
def recommended_jobs(request):
    profile = Profile.objects.filter(user=request.user).first()
    skills = _skill_tokens(profile.skills if profile else "")
    qs = Job.objects.all()

    # quick shortlist: any job that matches at least one skill in title or description
    q_filter = Q()
    for s in skills:
        q_filter |= Q(title__icontains=s) | Q(description__icontains=s)
    shortlisted = qs.filter(q_filter) if skills else qs.none()

    # score & sort in Python (simple, transparent)
    def score(job):
        text = (job.title + " " + job.description).lower()
        return sum(text.count(s) for s in skills)

    ranked = sorted(shortlisted, key=score, reverse=True)
    return render(request, "jobs/recommended.html", {
        "skills": skills,
        "jobs": ranked[:25],  # top 25
    })

def job_list(request):
    qs = Job.objects.all()
    q = request.GET.get
    
    # Basic filters
    if q("title"): 
        qs = qs.filter(title__icontains=q("title"))
    if q("location"): 
        qs = qs.filter(location__icontains=q("location"))
    if q("remote") == "1": 
        qs = qs.filter(is_remote=True)
    if q("visa") == "1": 
        qs = qs.filter(visa_sponsorship=True)
    if q("salary_min"): 
        qs = qs.filter(salary_min__gte=q("salary_min"))
    if q("salary_max"): 
        qs = qs.filter(salary_max__lte=q("salary_max"))
    
    # Location-based filtering with radius
    user_lat = q("user_lat")
    user_lon = q("user_lon")
    # Determine selected radius: query param, else user's commute radius, else empty
    radius_param = q("radius")
    radius_selected = None
    if radius_param:
        radius_selected = radius_param
    elif request.user.is_authenticated:
        try:
            radius_selected = str(Profile.objects.get(user=request.user).commute_radius_km)
        except Profile.DoesNotExist:
            radius_selected = None
    
    jobs_with_distance = []
    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            radius_value = float(radius_selected) if radius_selected else None
            
            for job in qs:
                if job.latitude and job.longitude:
                    distance = calculate_distance(user_lat, user_lon, job.latitude, job.longitude)
                    # Show all jobs with distance, but filter by radius if specified
                    if (radius_value is None) or (distance <= radius_value):
                        jobs_with_distance.append({
                            'job': job,
                            'distance': round(distance, 1)
                        })
                elif job.is_remote:
                    # Include remote jobs regardless of distance
                    jobs_with_distance.append({
                        'job': job,
                        'distance': 'Remote'
                    })
        except (ValueError, TypeError):
            # If coordinates are invalid, fall back to regular search
            jobs_with_distance = [{'job': job, 'distance': None} for job in qs]
    else:
        # No location filtering
        jobs_with_distance = [{'job': job, 'distance': None} for job in qs]
    
    return render(request, "jobs/job_list.html", {
        "jobs_with_distance": jobs_with_distance, 
        "filters": request.GET,
        "user_lat": user_lat,
        "user_lon": user_lon,
        "radius_selected": radius_selected,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(job=job, user=request.user).exists()
    return render(request, "jobs/job_detail.html", {
        "job": job,
        "has_applied": has_applied,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })

@login_required
@require_POST
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, user=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('jobs:detail', pk=pk)
    
    # Get note from form data
    note = request.POST.get('note', '')
    
    # Create application
    application = JobApplication.objects.create(job=job, user=request.user, note=note)
    messages.success(request, f"Successfully applied to {job.title}!")
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({
            'success': True,
            'message': f'Successfully applied to {job.title}!'
        })
    
    return redirect('jobs:detail', pk=pk)

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job').prefetch_related('status_history').order_by('-applied_at')
    
    # Calculate statistics
    stats = {
        'applied': applications.filter(status='applied').count(),
        'reviewed': applications.filter(status='reviewed').count(),
        'interview': applications.filter(status='interview').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    
    return render(request, "jobs/my_applications.html", {
        "applications": applications,
        "stats": stats,
    })

# Removed standalone map views; the Jobs list page includes an embedded map

@login_required
def post_job(request):
    """View for recruiters to post new job openings"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. Only recruiters can post jobs.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, f'Job "{job.title}" has been posted successfully!')
            return redirect('jobs:detail', pk=job.pk)
    else:
        form = JobPostForm()

    return render(request, 'jobs/job_post.html', {
        'form': form,
        'title': 'Post New Job',
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def edit_job(request, pk):
    """View for recruiters to edit existing job openings"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. Only recruiters can edit jobs.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            messages.success(request, f'Job "{job.title}" has been updated successfully!')
            return redirect('jobs:detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(request, 'jobs/job_post.html', {
        'form': form,
        'title': f'Edit Job: {job.title}',
        'job': job,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def my_jobs(request):
    """View for recruiters to see all their posted jobs"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    # For now, we'll show all jobs since we don't have a specific recruiter model
    # In a real application, you'd filter by the logged-in user
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {
        'jobs': jobs
    })


@login_required
def my_jobs_map(request):
    """Map view showing all recruiter's job postings with location pins"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    # Get all jobs with valid coordinates
    jobs = Job.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).order_by('-created_at')

    # Prepare job data for map markers
    jobs_data = []
    for job in jobs:
        applicant_count = JobApplication.objects.filter(job=job).count()
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company_name or 'Company',
            'location': job.location,
            'latitude': float(job.latitude),
            'longitude': float(job.longitude),
            'is_active': job.is_active,
            'applicant_count': applicant_count,
            'job_type': job.get_job_type_display() if job.job_type else 'N/A',
            'url': f'/jobs/{job.id}/'
        })

    import json
    return render(request, 'jobs/my_jobs_map.html', {
        'jobs_data_json': json.dumps(jobs_data),
        'total_jobs': len(jobs_data),
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def job_applicants(request, pk):
    """View for recruiters to see all applicants for a specific job"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    job = get_object_or_404(Job, pk=pk)
    applications = JobApplication.objects.filter(job=job).select_related('user', 'user__profile').order_by('-applied_at')

    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applications': applications
    })


@login_required
def job_applicants_map(request, job_id):
    """Map view showing applicant locations with clustering"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')

    job = get_object_or_404(Job, pk=job_id)
    applications = JobApplication.objects.filter(job=job).select_related('user', 'user__profile')

    # Prepare applicant data for map
    applicants_data = []
    for application in applications:
        try:
            candidate_profile = application.user.profile
            # Only include applicants with valid location coordinates
            if candidate_profile.latitude and candidate_profile.longitude:
                # Calculate distance from job location if available
                distance = None
                if job.latitude and job.longitude:
                    distance = _calculate_distance(
                        job.latitude, job.longitude,
                        candidate_profile.latitude, candidate_profile.longitude
                    )

                applicants_data.append({
                    'id': application.user.id,
                    'name': application.user.get_full_name() or application.user.username,
                    'email': application.user.email,
                    'username': application.user.username,
                    'headline': candidate_profile.headline or 'No headline',
                    'location': candidate_profile.location or 'Unknown',
                    'latitude': float(candidate_profile.latitude),
                    'longitude': float(candidate_profile.longitude),
                    'distance_km': int(distance) if distance else None,
                    'status': application.get_status_display(),
                    'status_class': application.status,
                    'applied_at': application.applied_at.strftime('%Y-%m-%d'),
                    'skills': candidate_profile.skills[:100] if candidate_profile.skills else 'Not specified',
                    'profile_url': f'/accounts/u/{application.user.username}/'
                })
        except Profile.DoesNotExist:
            continue

    # Calculate statistics
    total_applicants = len(applicants_data)
    avg_distance = None
    within_radius = 0
    location_stats = {}

    if applicants_data and job.latitude and job.longitude:
        distances = [a['distance_km'] for a in applicants_data if a['distance_km']]
        if distances:
            avg_distance = int(sum(distances) / len(distances))
            # Assume 50km as reasonable commute radius
            within_radius = sum(1 for d in distances if d <= 50)

        # Count applicants by city
        for applicant in applicants_data:
            city = applicant['location'].split(',')[0].strip()
            location_stats[city] = location_stats.get(city, 0) + 1

    # Get top 5 cities
    top_cities = sorted(location_stats.items(), key=lambda x: x[1], reverse=True)[:5]

    import json
    return render(request, 'jobs/job_applicants_map.html', {
        'job': job,
        'applicants_data_json': json.dumps(applicants_data),
        'total_applicants': total_applicants,
        'total_applications': applications.count(),
        'avg_distance': avg_distance,
        'within_radius': within_radius,
        'top_cities': top_cities,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })


@login_required
def job_candidate_recommendations(request, job_id):
    """Get recommended candidates for a specific job posting"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            return JsonResponse({'error': 'Access denied'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    job = get_object_or_404(Job, pk=job_id)

    # Extract job requirements
    job_skills = _skill_tokens(job.required_skills or job.description)
    job_location = job.location
    job_lat = job.latitude
    job_lon = job.longitude

    # Get all job seekers who haven't applied yet
    existing_applicants = JobApplication.objects.filter(job=job).values_list('user_id', flat=True)
    job_seekers = User.objects.filter(
        profile__user_type='job_seeker',
        profile__is_public=True
    ).exclude(id__in=existing_applicants).select_related('profile')

    candidates = []

    for user in job_seekers:
        try:
            candidate_profile = user.profile
        except Profile.DoesNotExist:
            continue

        match_score = 0
        match_reasons = []

        # Skills matching (highest priority)
        if job_skills and candidate_profile.skills:
            user_skills = _skill_tokens(candidate_profile.skills)
            skill_matches = set(job_skills) & set(user_skills)
            if skill_matches:
                match_score += len(skill_matches) * 10
                match_reasons.append(f"{len(skill_matches)} matching skill(s): {', '.join(list(skill_matches)[:3])}")

        # Education matching
        if candidate_profile.education and job.description:
            education_lower = candidate_profile.education.lower()
            job_desc_lower = job.description.lower()
            # Look for degree keywords in job description
            degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'degree', 'university', 'college']
            education_mentions = sum(1 for keyword in degree_keywords if keyword in job_desc_lower and keyword in education_lower)
            if education_mentions > 0:
                match_score += education_mentions * 5
                match_reasons.append(f"Relevant education background")

        # Experience matching
        if candidate_profile.experience and job.description:
            experience_lower = candidate_profile.experience.lower()
            job_desc_lower = job.description.lower()
            # Extract experience keywords from job description
            experience_keywords = re.findall(r'\b[a-z]+\b', job_desc_lower)
            experience_matches = sum(1 for keyword in experience_keywords if len(keyword) > 4 and keyword in experience_lower)
            if experience_matches > 5:  # Threshold to avoid noise
                match_score += min(experience_matches, 10) * 3  # Cap contribution
                match_reasons.append(f"Relevant work experience")

        # Location proximity (bonus points)
        if job_lat and job_lon and candidate_profile.latitude and candidate_profile.longitude:
            distance_km = _calculate_distance(job_lat, job_lon, candidate_profile.latitude, candidate_profile.longitude)
            if distance_km is not None:
                # Closer candidates get bonus points (max 20 points for <5km, decreasing)
                if distance_km < 5:
                    proximity_score = 20
                elif distance_km < 25:
                    proximity_score = 15
                elif distance_km < 50:
                    proximity_score = 10
                elif distance_km < 100:
                    proximity_score = 5
                else:
                    proximity_score = 2

                match_score += proximity_score
                match_reasons.append(f"Located {int(distance_km)} km from job location")
        elif job_location and candidate_profile.location:
            # Fallback to text-based location matching
            if job_location.lower() in candidate_profile.location.lower():
                match_score += 5
                match_reasons.append(f"Located in {candidate_profile.location}")

        # Experience level alignment
        if job.experience_level and candidate_profile.experience:
            experience_text = candidate_profile.experience.lower()
            level_keywords = {
                'entry': ['entry', 'junior', 'graduate', 'intern'],
                'mid': ['mid', 'intermediate', '2 years', '3 years', '4 years'],
                'senior': ['senior', 'lead', '5 years', '6 years', '7+ years'],
                'lead': ['lead', 'principal', 'manager', 'architect'],
                'executive': ['director', 'vp', 'cto', 'ceo', 'executive']
            }

            expected_keywords = level_keywords.get(job.experience_level, [])
            if any(keyword in experience_text for keyword in expected_keywords):
                match_score += 5
                match_reasons.append(f"Experience level matches {job.get_experience_level_display()}")

        # Only include candidates with meaningful matches
        if match_score > 0:
            candidates.append({
                'user': user,
                'profile': candidate_profile,
                'match_score': match_score,
                'match_reasons': match_reasons
            })

    # Sort by match score (highest first)
    candidates.sort(key=lambda x: x['match_score'], reverse=True)

    # Return top 25 candidates
    top_candidates = candidates[:25]

    # Format for JSON response
    recommendations = []
    for candidate in top_candidates:
        recommendations.append({
            'id': candidate['user'].id,
            'username': candidate['user'].username,
            'name': candidate['user'].get_full_name() or candidate['user'].username,
            'headline': candidate['profile'].headline or 'No headline',
            'location': candidate['profile'].location or 'Not specified',
            'skills': candidate['profile'].skills[:100] if candidate['profile'].skills else 'Not specified',
            'match_score': candidate['match_score'],
            'match_reasons': candidate['match_reasons'],
            'profile_url': f"/accounts/u/{candidate['user'].username}/"
        })

    return JsonResponse({
        'success': True,
        'job_title': job.title,
        'total_recommendations': len(recommendations),
        'recommendations': recommendations
    })


@login_required
@require_POST
def update_application_status(request, application_id):
    """Update application status and send message to candidate"""
    try:
        import json
        data = json.loads(request.body)
        new_status = data.get('status')
        
        # Get the application
        application = get_object_or_404(JobApplication, id=application_id)
        
        # Check if user is authorized (recruiter or job owner)
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        # Store old status for comparison
        old_status = application.status
        
        # Only proceed if status actually changed
        if old_status != new_status:
            # Update status
            application.status = new_status
            application.save()
            
            # Create status history record
            from jobs.models import ApplicationStatusHistory
            ApplicationStatusHistory.objects.create(
                application=application,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user
            )
            
            # Send message to candidate about status change
            from accounts.models import Message
            
            status_messages = {
                'applied': 'Your application has been received and is being reviewed.',
                'reviewed': 'Great news! Your application is under review by our team.',
                'interview': '🎉 Congratulations! We would like to schedule an interview with you for the {job_title} position.',
                'accepted': '🎊 Congratulations! We are pleased to offer you the {job_title} position!',
                'rejected': 'Thank you for your interest in the {job_title} position. After careful consideration, we have decided to move forward with other candidates.',
            }
            
            subject = f'Update on your application for {application.job.title}'
            body = status_messages.get(new_status, 'Your application status has been updated.').format(
                job_title=application.job.title
            )
            
            # Add additional context
            body += f'\n\nStatus: {application.get_status_display()}'
            body += f'\nCompany: {application.job.company_name or "Our Company"}'
            body += f'\n\nIf you have any questions, please reply to this message.'
            
            # Create the message
            Message.objects.create(
                sender=request.user,
                recipient=application.user,
                subject=subject,
                body=body,
                job_application=application
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated to {application.get_status_display()} and notification sent to candidate',
            'new_status': new_status,
            'new_status_display': application.get_status_display()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search_candidates(request):
    """API endpoint to search for candidates (job seekers)"""
    query = request.GET.get('search', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'candidates': []})
    
    # Search for job seekers by username, email, or profile info
    from django.contrib.auth.models import User
    from accounts.models import Profile
    
    # Get all job seekers
    job_seekers = User.objects.filter(
        profile__user_type='job_seeker'
    ).select_related('profile')
    
    # Filter by search query
    candidates = []
    for user in job_seekers:
        if (query.lower() in user.username.lower() or 
            query.lower() in user.email.lower() or
            (user.first_name and query.lower() in user.first_name.lower()) or
            (user.last_name and query.lower() in user.last_name.lower()) or
            (user.profile.headline and query.lower() in user.profile.headline.lower())):
            
            candidates.append({
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'username': user.username
            })
    
    return JsonResponse({'candidates': candidates[:10]})  # Limit to 10 results


# Pipeline Management Views
@login_required
def pipeline_management(request, job_id):
    """Kanban board view for managing job application pipeline"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')
    
    job = get_object_or_404(Job, pk=job_id)
    applications = JobApplication.objects.filter(job=job).select_related('user', 'user__profile')
    
    # Get or create default pipeline stages
    stages = PipelineStage.objects.filter(is_active=True).order_by('order')
    if not stages.exists():
        # Create default stages
        default_stages = [
            {'name': 'Applied', 'order': 1, 'color': '#6c757d'},
            {'name': 'Screening', 'order': 2, 'color': '#ffc107'},
            {'name': 'Interview', 'order': 3, 'color': '#17a2b8'},
            {'name': 'Final Review', 'order': 4, 'color': '#28a745'},
            {'name': 'Hired', 'order': 5, 'color': '#007bff'},
        ]
        for stage_data in default_stages:
            PipelineStage.objects.get_or_create(
                name=stage_data['name'],
                defaults=stage_data
            )
        stages = PipelineStage.objects.filter(is_active=True).order_by('order')
    
    # Get applications with their pipeline positions
    applications_with_stages = []
    for app in applications:
        try:
            pipeline = app.pipeline
            stage = pipeline.stage
        except ApplicationPipeline.DoesNotExist:
            # Assign to first stage if not in pipeline
            stage = stages.first()
            if stage:
                ApplicationPipeline.objects.create(application=app, stage=stage)
        
        applications_with_stages.append({
            'application': app,
            'stage': stage,
            'pipeline': getattr(app, 'pipeline', None)
        })
    
    return render(request, 'jobs/pipeline_management.html', {
        'job': job,
        'stages': stages,
        'applications_with_stages': applications_with_stages
    })


@login_required
@require_POST
def move_application_stage(request, application_id):
    """Move an application to a different pipeline stage"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            return JsonResponse({'error': 'Access denied'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    
    application = get_object_or_404(JobApplication, pk=application_id)
    stage_id = request.POST.get('stage_id')
    notes = request.POST.get('notes', '')
    
    if not stage_id:
        return JsonResponse({'error': 'Stage ID required'}, status=400)
    
    try:
        stage = PipelineStage.objects.get(pk=stage_id, is_active=True)
    except PipelineStage.DoesNotExist:
        return JsonResponse({'error': 'Invalid stage'}, status=400)
    
    # Update or create pipeline entry
    pipeline, created = ApplicationPipeline.objects.get_or_create(
        application=application,
        defaults={'stage': stage, 'notes': notes}
    )
    
    old_stage = None
    if not created:
        old_stage = pipeline.stage
        pipeline.stage = stage
        pipeline.notes = notes
        pipeline.save()
    
    # Map pipeline stage names to application statuses (case-insensitive)
    stage_name_lower = stage.name.lower()
    
    # Determine new status based on stage name keywords
    if 'applied' in stage_name_lower or 'new' in stage_name_lower:
        new_status = 'applied'
    elif 'screen' in stage_name_lower or 'review' in stage_name_lower:
        new_status = 'reviewed'
    elif 'interview' in stage_name_lower:
        new_status = 'interview'
    elif 'hired' in stage_name_lower or 'accept' in stage_name_lower or 'offer' in stage_name_lower:
        new_status = 'accepted'
    elif 'reject' in stage_name_lower or 'declined' in stage_name_lower:
        new_status = 'rejected'
    else:
        # Default mapping for exact matches
        stage_to_status_map = {
            'Applied': 'applied',
            'Screening': 'reviewed',
            'Interview': 'interview',
            'Final Review': 'reviewed',
            'Hired': 'accepted',
            'Rejected': 'rejected',
        }
        new_status = stage_to_status_map.get(stage.name, None)
    old_status = application.status
    
    if new_status and new_status != old_status:
        application.status = new_status
        application.save()
        
        # Create status history record
        from jobs.models import ApplicationStatusHistory
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user
        )
        
        # Send message to candidate about status change
        from accounts.models import Message
        
        status_messages = {
            'applied': 'Your application has been received and is being reviewed.',
            'reviewed': 'Great news! Your application is under review by our team.',
            'interview': '🎉 Congratulations! We would like to schedule an interview with you for the {job_title} position. Please check your email or reply to this message to coordinate scheduling.',
            'accepted': '🎊 Congratulations! We are pleased to offer you the {job_title} position! We will be in touch with next steps.',
            'rejected': 'Thank you for your interest in the {job_title} position. After careful consideration, we have decided to move forward with other candidates. We appreciate the time you invested in the application process.',
        }
        
        subject = f'Update on your application for {application.job.title}'
        body = status_messages.get(new_status, 'Your application status has been updated.').format(
            job_title=application.job.title
        )
        
        # Add additional context
        body += f'\n\nStatus: {application.get_status_display()}'
        body += f'\nCompany: {application.job.company_name or "Our Company"}'
        if notes:
            body += f'\n\nAdditional Notes: {notes}'
        body += f'\n\nIf you have any questions, please reply to this message.'
        
        # Create the message
        Message.objects.create(
            sender=request.user,
            recipient=application.user,
            subject=subject,
            body=body,
            job_application=application
        )
    
    return JsonResponse({
        'success': True,
        'message': f'Application moved to {stage.name}' + (f' and status updated to {application.get_status_display()}' if new_status and new_status != old_status else ''),
        'stage_name': stage.name,
        'stage_color': stage.color,
        'status_updated': new_status is not None and new_status != old_status
    })


# Candidate Search Views
@login_required
def candidate_search(request):
    """Advanced candidate search interface for recruiters"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')
    
    # Get search parameters
    skills = request.GET.get('skills', '').strip()
    location = request.GET.get('location', '').strip()
    radius = request.GET.get('radius', '50')
    education = request.GET.get('education', '').strip()
    experience = request.GET.get('experience', '').strip()
    
    candidates = []

    if any([skills, location, education, experience]):
        # Get job seekers
        job_seekers = User.objects.filter(
            profile__user_type='job_seeker',
            profile__is_public=True
        ).select_related('profile')

        for user in job_seekers:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                continue

            match_reasons = []
            has_match = False  # Changed to OR logic: matches ANY criterion

            # Skills matching (OR logic - if ANY skill matches)
            if skills:
                try:
                    user_skills = _skill_tokens(profile.skills or '')
                    search_skills = _skill_tokens(skills)
                    skill_matches = set(user_skills) & set(search_skills)
                    if skill_matches:
                        has_match = True
                        matching_skills = ', '.join(list(skill_matches)[:5])
                        if len(skill_matches) > 5:
                            matching_skills += f" (+{len(skill_matches) - 5} more)"
                        match_reasons.append(f"Matching skills: {matching_skills}")
                except Exception:
                    pass

            # Education matching (OR logic - if ANY keyword matches)
            if education:
                try:
                    # Check both old text field and new structured entries
                    education_match = False
                    if profile.education:
                        education_lower = profile.education.lower()
                        education_keywords = education.lower().split()
                        if any(keyword in education_lower for keyword in education_keywords):
                            education_match = True

                    # Also check structured education entries
                    for edu in profile.education_entries.all():
                        edu_text = f"{edu.school_name} {edu.degree} {edu.field_of_study}".lower()
                        if any(keyword in edu_text for keyword in education.lower().split()):
                            education_match = True
                            break

                    if education_match:
                        has_match = True
                        match_reasons.append(f"Education background matches search")
                except Exception:
                    pass

            # Experience matching (OR logic - if ANY keyword matches)
            if experience:
                try:
                    # Check both old text field and new structured entries
                    experience_match = False
                    if profile.experience:
                        experience_lower = profile.experience.lower()
                        experience_keywords = experience.lower().split()
                        if any(keyword in experience_lower for keyword in experience_keywords):
                            experience_match = True

                    # Also check structured work experience entries
                    for work in profile.work_experiences.all():
                        work_text = f"{work.job_title} {work.company_name} {work.description}".lower()
                        if any(keyword in work_text for keyword in experience.lower().split()):
                            experience_match = True
                            break

                    if experience_match:
                        has_match = True
                        match_reasons.append(f"Work experience matches search")
                except Exception:
                    pass

            # Location matching (OR logic - if location matches)
            if location:
                location_match = False
                try:
                    # Try distance-based matching if coordinates are available
                    search_lat, search_lon = _get_coordinates_from_location(location)
                    profile_lat = profile.latitude
                    profile_lon = profile.longitude

                    if not profile_lat or not profile_lon:
                        profile_lat, profile_lon = _get_coordinates_from_location(profile.location)

                    # If we have coordinates for both, calculate distance
                    if search_lat and search_lon and profile_lat and profile_lon:
                        distance_km = _calculate_distance(search_lat, search_lon, profile_lat, profile_lon)
                        radius_km = int(radius) if radius.isdigit() else 50

                        if distance_km <= radius_km:
                            location_match = True
                            has_match = True
                            match_reasons.append(f"Location: {profile.location} ({int(distance_km)} km away)")
                    else:
                        # Fallback to text-based matching if no coordinates
                        if profile.location:
                            location_lower = location.lower()
                            profile_location_lower = profile.location.lower()

                            if (location_lower in profile_location_lower or
                                profile_location_lower in location_lower or
                                any(word in profile_location_lower for word in location_lower.split(','))):
                                location_match = True
                                has_match = True
                                match_reasons.append(f"Location: {profile.location}")
                except Exception:
                    pass

            # Include candidate if they match ANY search criterion (OR logic)
            if has_match:
                candidates.append({
                    'user': user,
                    'profile': profile,
                    'match_reasons': match_reasons
                })
    
    return render(request, 'jobs/candidate_search.html', {
        'candidates': candidates,
        'search_params': {
            'skills': skills,
            'location': location,
            'radius': radius,
            'education': education,
            'experience': experience
        }
    })


@login_required
def saved_searches(request):
    """Manage saved candidate searches"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')
    
    searches = SavedSearch.objects.filter(recruiter=request.user).order_by('-created_at')
    
    return render(request, 'jobs/saved_searches.html', {
        'searches': searches
    })


@login_required
@require_POST
def save_search(request):
    """Save a candidate search for future use"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            return JsonResponse({'error': 'Access denied'}, status=403)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    
    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    skills = request.POST.get('skills', '').strip()
    location = request.POST.get('location', '').strip()
    radius = request.POST.get('radius', '50')
    education = request.POST.get('education', '').strip()
    experience = request.POST.get('experience', '').strip()
    notify = request.POST.get('notify') == 'on'
    
    if not name:
        return JsonResponse({'error': 'Search name is required'}, status=400)
    
    # Create saved search
    saved_search = SavedSearch.objects.create(
        recruiter=request.user,
        name=name,
        description=description,
        skills=skills,
        location=location,
        location_radius=int(radius) if radius.isdigit() else 50,
        education_keywords=education,
        experience_keywords=experience,
        notify_on_new_matches=notify
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Search saved successfully',
        'search_id': saved_search.id
    })


@login_required
def run_saved_search(request, search_id):
    """Run a saved search and show results"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')
    
    saved_search = get_object_or_404(SavedSearch, pk=search_id, recruiter=request.user)
    
    # Build search parameters
    search_params = {
        'skills': saved_search.skills,
        'location': saved_search.location,
        'radius': str(saved_search.location_radius),
        'education': saved_search.education_keywords,
        'experience': saved_search.experience_keywords
    }
    
    # Redirect to candidate search with parameters
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from urllib.parse import urlencode
    
    url = reverse('jobs:candidate_search') + '?' + urlencode({k: v for k, v in search_params.items() if v})
    return HttpResponseRedirect(url)


@login_required
def search_notifications(request):
    """View saved search notifications for recruiters"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect('core:home')
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup first.")
        return redirect('accounts:profile')
    
    # Get notifications for this recruiter's saved searches
    notifications = SearchNotification.objects.filter(
        saved_search__recruiter=request.user
    ).select_related('candidate', 'candidate__profile', 'saved_search').order_by('-sent_at')
    
    return render(request, 'jobs/search_notifications.html', {
        'notifications': notifications
    })


@login_required
@require_POST
def trigger_saved_search_check(request):
    """Manually trigger saved search check for new matches (for testing)"""
    try:
        # Check if user is a recruiter
        try:
            profile = Profile.objects.get(user=request.user)
            if not profile.is_recruiter:
                return JsonResponse({'error': 'Access denied'}, status=403)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)
        
        # Get all saved searches for this recruiter with notifications enabled
        saved_searches = SavedSearch.objects.filter(
            recruiter=request.user,
            notify_on_new_matches=True
        )
        
        if not saved_searches.exists():
            return JsonResponse({
                'success': False,
                'message': 'No saved searches with notifications enabled'
            })
        
        total_new_matches = 0
        
        for search in saved_searches:
            # Get job seekers
            job_seekers = User.objects.filter(
                profile__user_type='job_seeker',
                profile__is_public=True
            ).select_related('profile')
            
            for user in job_seekers:
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    continue
                
                # Check if we've already notified about this candidate
                if SearchNotification.objects.filter(
                    saved_search=search,
                    candidate=user
                ).exists():
                    continue
                
                # Calculate match score using the same logic as candidate_search
                match_score = 0
                
                # Skills matching
                if search.skills and profile.skills:
                    try:
                        user_skills = _skill_tokens(profile.skills or '')
                        search_skills = _skill_tokens(search.skills)
                        skill_matches = len(set(user_skills) & set(search_skills))
                        if skill_matches > 0:
                            match_score += skill_matches * 10
                    except Exception:
                        pass
                
                # Education matching
                if search.education_keywords and profile.education:
                    education_lower = profile.education.lower()
                    education_keywords = search.education_keywords.lower().split()
                    matches = sum(1 for keyword in education_keywords if keyword in education_lower)
                    if matches > 0:
                        match_score += matches * 5
                
                # Experience matching
                if search.experience_keywords and profile.experience:
                    experience_lower = profile.experience.lower()
                    experience_keywords = search.experience_keywords.lower().split()
                    matches = sum(1 for keyword in experience_keywords if keyword in experience_lower)
                    if matches > 0:
                        match_score += matches * 5
                
                # Location matching
                if search.location and profile.location:
                    location_lower = search.location.lower()
                    profile_location_lower = profile.location.lower()
                    
                    if (location_lower in profile_location_lower or 
                        profile_location_lower in location_lower or
                        any(word in profile_location_lower for word in location_lower.split(','))):
                        match_score += 5
                
                # If there's a match, send notification
                if match_score > 0:
                    # Build match details
                    match_details = []
                    if profile.skills:
                        match_details.append(f"Skills: {profile.skills[:100]}")
                    if profile.location:
                        match_details.append(f"Location: {profile.location}")
                    if profile.education:
                        match_details.append(f"Education: {profile.education[:100]}")
                    
                    details_text = '\n'.join(f"• {detail}" for detail in match_details[:3])
                    
                    subject = f'New candidate match for "{search.name}"'
                    body = f'''A new candidate matches your saved search "{search.name}"!

Candidate: {user.get_full_name() or user.username}
Match Score: {match_score} points

{details_text}

View their profile at: /accounts/profile/{user.username}/

Click here to view all notifications for this search.
'''
                    
                    # Create in-platform message
                    Message.objects.create(
                        sender=request.user,
                        recipient=request.user,
                        subject=subject,
                        body=body
                    )
                    
                    # Create notification record
                    SearchNotification.objects.create(
                        saved_search=search,
                        candidate=user
                    )
                    
                    total_new_matches += 1
            
            # Update last_notified timestamp
            if total_new_matches > 0:
                search.last_notified = timezone.now()
                search.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Found {total_new_matches} new candidate matches!',
            'new_matches': total_new_matches
        })
    
    except Exception as e:
        # Return detailed error for debugging
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': f'An error occurred while checking for matches: {str(e)}'
        }, status=500)
