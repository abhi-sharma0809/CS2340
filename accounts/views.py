from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
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
    return render(request, "accounts/signup.html", {"form": form})

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
