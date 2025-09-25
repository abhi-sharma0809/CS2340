from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'salary_min', 'salary_max', 'is_remote', 'visa_sponsorship', 'created_at']
    list_filter = ['is_remote', 'visa_sponsorship', 'created_at']
    search_fields = ['title', 'company_name', 'location', 'description']
    list_editable = ['salary_min', 'salary_max', 'is_remote', 'visa_sponsorship']
    ordering = ['-created_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'job__title', 'job__company_name']
    ordering = ['-applied_at']
