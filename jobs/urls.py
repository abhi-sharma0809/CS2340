from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="list"),
    path("<int:pk>/", views.job_detail, name="detail"),
    path("<int:pk>/apply/", views.apply_job, name="apply"),
    path("recommended/", views.recommended_jobs, name="recommended"),
    path("my-applications/", views.my_applications, name="my_applications"),
    # Removed standalone map routes; map functionality lives on the Jobs list page
]
