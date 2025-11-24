from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="list"),
    path("<int:pk>/", views.job_detail, name="detail"),
    path("<int:pk>/apply/", views.apply_job, name="apply"),
    path("recommended/", views.recommended_jobs, name="recommended"),
    path("my-applications/", views.my_applications, name="my_applications"),
    # Recruiter views
    path("post/", views.post_job, name="post"),
    path("<int:pk>/edit/", views.edit_job, name="edit"),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("<int:pk>/applicants/", views.job_applicants, name="applicants"),
    path("api/update-application-status/<int:application_id>/", views.update_application_status, name="update_application_status"),
    # API endpoints
    path("api/candidates/", views.search_candidates, name="search_candidates"),
    # Removed standalone map routes; map functionality lives on the Jobs list page
    
    # New recruiter functionality
    path("<int:job_id>/pipeline/", views.pipeline_management, name="pipeline_management"),
    path("api/move-application/<int:application_id>/", views.move_application_stage, name="move_application_stage"),
    path("candidate-search/", views.candidate_search, name="candidate_search"),
    path("saved-searches/", views.saved_searches, name="saved_searches"),
    path("api/save-search/", views.save_search, name="save_search"),
    path("saved-search/<int:search_id>/", views.run_saved_search, name="run_saved_search"),
    path("search-notifications/", views.search_notifications, name="search_notifications"),
    path("api/trigger-saved-search-check/", views.trigger_saved_search_check, name="trigger_saved_search_check"),
]
