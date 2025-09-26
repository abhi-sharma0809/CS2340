from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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
