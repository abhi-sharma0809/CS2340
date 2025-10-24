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
    
    # Communication URLs (CRM-22 & CRM-23)
    path("send-message/<int:recipient_id>/", views.send_message, name="send_message"),
    path("send-email/<int:recipient_id>/", views.send_email, name="send_email"),
    path("messages/", views.get_messages, name="get_messages"),
    path("emails/", views.get_emails, name="get_emails"),
    path("mark-read/<int:message_id>/", views.mark_message_read, name="mark_message_read"),
]