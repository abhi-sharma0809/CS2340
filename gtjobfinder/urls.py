from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout/password views
    path("jobs/", include(("jobs.urls", "jobs"), namespace="jobs")),
    path("", include(("core.urls", "core"), namespace="core")),]