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
    # API endpoints
    path("api/candidates/", views.search_candidates, name="search_candidates"),
    # Removed standalone map routes; map functionality lives on the Jobs list page
]
