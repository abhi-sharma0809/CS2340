# accounts/models.py
from django.conf import settings
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    
    # Job seeker specific fields
    headline = models.CharField(max_length=120, blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    links = models.TextField(blank=True)

    # Privacy
    is_public = models.BooleanField(default=True)  # global gate
    show_skills = models.BooleanField(default=True)
    show_education = models.BooleanField(default=True)
    show_experience = models.BooleanField(default=True)
    show_links = models.BooleanField(default=True)

    commute_radius_km = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def is_job_seeker(self):
        return self.user_type == 'job_seeker'
    
    @property
    def is_recruiter(self):
        return self.user_type == 'recruiter'

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    company_website = models.URLField(blank=True)
    company_logo = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"


class Message(models.Model):
    """In-platform messaging between recruiters and job seekers"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Optional: Link to job application for context
    job_application = models.ForeignKey('jobs.JobApplication', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.subject}"


class EmailLog(models.Model):
    """Track emails sent through the platform"""
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_emails')
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    
    # Optional: Link to job application for context
    job_application = models.ForeignKey('jobs.JobApplication', on_delete=models.SET_NULL, null=True, blank=True, related_name='emails')
    
    # External service tracking
    external_message_id = models.CharField(max_length=200, blank=True, help_text="ID from email service provider")
    error_message = models.TextField(blank=True, help_text="Error details if sending failed")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Email from {self.sender.username} to {self.recipient_email}: {self.subject}"
