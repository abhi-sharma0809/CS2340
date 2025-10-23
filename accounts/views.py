from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, RecruiterProfile
from .forms import ProfileForm, RecruiterRegistrationForm, RecruiterProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # create blank profile
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def view_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile_detail.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile_form.html", {"form": form})

def public_profile(request, username):
    owner = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=owner)
    if not profile.is_public and request.user != owner:
        return HttpResponseForbidden("This profile is private.")
    return render(request, "accounts/public_profile.html", {"owner": owner, "profile": profile})

def recruiter_signup(request):
    """Registration form specifically for recruiters"""
    if request.method == "POST":
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile with recruiter type
            profile, _ = Profile.objects.get_or_create(user=user, user_type='recruiter')
            login(request, user)
            messages.success(request, "Welcome! Please complete your company profile.")
            return redirect("accounts:recruiter_profile")
        else:
            # Form is not valid, show errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecruiterRegistrationForm()
    return render(request, "registration/recruiter_signup.html", {"form": form})

@login_required
def recruiter_profile(request):
    """View and edit recruiter company profile"""
    try:
        recruiter_profile = request.user.recruiter_profile
    except RecruiterProfile.DoesNotExist:
        recruiter_profile = None
    
    if request.method == "POST":
        if recruiter_profile:
            form = RecruiterProfileForm(request.POST, instance=recruiter_profile)
        else:
            form = RecruiterProfileForm(request.POST)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Company profile updated successfully!")
            return redirect("accounts:recruiter_profile")
    else:
        if recruiter_profile:
            form = RecruiterProfileForm(instance=recruiter_profile)
        else:
            form = RecruiterProfileForm()
    
    return render(request, "accounts/recruiter_profile.html", {
        "form": form,
        "recruiter_profile": recruiter_profile
    })

@login_required
def recruiter_dashboard(request):
    """Main dashboard for recruiters"""
    # Check if user is a recruiter
    try:
        profile = Profile.objects.get(user=request.user)
        if not profile.is_recruiter:
            messages.error(request, "Access denied. This area is for recruiters only.")
            return redirect("core:home")
    except Profile.DoesNotExist:
        messages.error(request, "Please complete your profile setup.")
        return redirect("accounts:profile")
    
    # Get recruiter profile
    try:
        recruiter_profile = request.user.recruiter_profile
    except RecruiterProfile.DoesNotExist:
        recruiter_profile = None
    
    # Get recruiter's jobs (for now, all jobs since we don't have job ownership yet)
    from jobs.models import Job, JobApplication
    jobs = Job.objects.all().order_by('-created_at')[:10]  # Recent jobs
    total_applications = JobApplication.objects.count()
    
    return render(request, "accounts/recruiter_dashboard.html", {
        "recruiter_profile": recruiter_profile,
        "jobs": jobs,
        "total_applications": total_applications
    })
