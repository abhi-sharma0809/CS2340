from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),     # optional simple signup
    path("recruiter-signup/", views.recruiter_signup, name="recruiter_signup"),
    path("profile/", views.view_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="profile_edit"),
    path("recruiter-profile/", views.recruiter_profile, name="recruiter_profile"),
    path("recruiter-dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("u/<str:username>/", views.public_profile, name="public_profile"),
]