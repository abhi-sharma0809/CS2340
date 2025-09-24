from django.urls import path
from . import views
urlpatterns = [
    path("", views.job_list, name="list"),
    path("<int:pk>/", views.job_detail, name="detail"),
    path("recommended/", views.recommended_jobs, name="recommended"),
]
