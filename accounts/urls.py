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
    path("messages-page/", views.messages_page, name="messages_page"),
    path("recruiter-messages/", views.recruiter_messages_page, name="recruiter_messages_page"),
    path("send-reply/", views.send_reply, name="send_reply"),
    path("emails/", views.get_emails, name="get_emails"),
    path("mark-read/<int:message_id>/", views.mark_message_read, name="mark_message_read"),
    
    # Admin URLs
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/users/", views.admin_users, name="admin_users"),
    path("admin/users/<int:user_id>/toggle-status/", views.admin_toggle_user_status, name="admin_toggle_user_status"),
    path("admin/users/<int:user_id>/change-role/", views.admin_change_user_role, name="admin_change_user_role"),
    path("admin/users/<int:user_id>/delete/", views.admin_delete_user, name="admin_delete_user"),
    path("admin/jobs/", views.admin_jobs, name="admin_jobs"),
    path("admin/jobs/<int:job_id>/toggle-status/", views.admin_toggle_job_status, name="admin_toggle_job_status"),
    path("admin/jobs/<int:job_id>/delete/", views.admin_delete_job, name="admin_delete_job"),
    path("admin/export/", views.admin_export_data, name="admin_export_data"),
]