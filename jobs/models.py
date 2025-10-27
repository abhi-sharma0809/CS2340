from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Job(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120, blank=True)
    # Location coordinates for distance calculation
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude coordinate")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude coordinate")
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Company information
    company_name = models.CharField(max_length=120, blank=True)
    company_logo = models.URLField(blank=True, help_text="URL to company logo image")
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company_name or 'Unknown Company'}"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, help_text="Optional note from the applicant")
    status = models.CharField(
        max_length=20,
        choices=[
            ('applied', 'Applied'),
            ('reviewed', 'Under Review'),
            ('interview', 'Interview Scheduled'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted'),
        ],
        default='applied'
    )
    
    class Meta:
        unique_together = ['job', 'user']  # Prevent duplicate applications
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"


class ApplicationStatusHistory(models.Model):
    """Track status changes for job applications"""
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='status_changes_made')
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Application status histories'
    
    def __str__(self):
        return f"{self.application.user.username} - {self.old_status} → {self.new_status}"


# Pipeline Management Models
class PipelineStage(models.Model):
    """Customizable pipeline stages for managing job applications"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class ApplicationPipeline(models.Model):
    """Track applications through custom pipeline stages"""
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='pipeline')
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, related_name='applications')
    moved_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Internal notes about this stage")
    
    class Meta:
        ordering = ['-moved_at']
    
    def __str__(self):
        return f"{self.application.user.username} - {self.stage.name}"


# Candidate Search Models
class SavedSearch(models.Model):
    """Saved candidate searches for recruiters"""
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Search criteria
    skills = models.TextField(blank=True, help_text="Comma-separated skills to search for")
    location = models.CharField(max_length=120, blank=True)
    location_radius = models.PositiveIntegerField(default=50, help_text="Radius in kilometers")
    education_keywords = models.TextField(blank=True, help_text="Education keywords to search for")
    experience_keywords = models.TextField(blank=True, help_text="Experience keywords to search for")
    
    # Notification settings
    notify_on_new_matches = models.BooleanField(default=True)
    last_notified = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recruiter.username} - {self.name}"


class SearchNotification(models.Model):
    """Track notifications sent for saved searches"""
    saved_search = models.ForeignKey(SavedSearch, on_delete=models.CASCADE, related_name='notifications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_notifications')
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['saved_search', 'candidate']
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Notification for {self.candidate.username} - {self.saved_search.name}"
