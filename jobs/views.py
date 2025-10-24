import re
import math
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Job, JobApplication
from .forms import JobPostForm
from accounts.models import Profile

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
    applications = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, "jobs/my_applications.html", {
        "applications": applications
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
        'title': 'Post New Job'
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
        'job': job
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
