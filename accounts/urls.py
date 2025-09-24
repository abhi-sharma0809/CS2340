from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),     # optional simple signup
    path("profile/", views.view_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="profile_edit"),
    path("u/<str:username>/", views.public_profile, name="public_profile"),

]