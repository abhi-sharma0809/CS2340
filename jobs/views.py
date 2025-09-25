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
    radius = q("radius")
    
    jobs_with_distance = []
    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            radius = float(radius) if radius else 50  # Default 50km radius if not specified
            
            for job in qs:
                if job.latitude and job.longitude:
                    distance = calculate_distance(user_lat, user_lon, job.latitude, job.longitude)
                    # Show all jobs with distance, but filter by radius if specified
                    if not radius or distance <= radius:
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
        "radius": radius,
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
    
    # Create application
    application = JobApplication.objects.create(job=job, user=request.user)
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

def map_test(request):
    return render(request, "jobs/map_test.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })

def location_test(request):
    return render(request, "jobs/location_test.html")
