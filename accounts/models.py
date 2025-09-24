from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=120, blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    links = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    commute_radius_km = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.user.username}'s profile"
