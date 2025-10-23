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
    # Removed standalone map routes; map functionality lives on the Jobs list page
]
