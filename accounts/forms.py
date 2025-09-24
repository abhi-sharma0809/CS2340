# accounts/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "headline", "skills", "education", "experience", "links",
            "is_public", "show_skills", "show_education", "show_experience", "show_links",
            "commute_radius_km",
        ]
        help_texts = {
            "is_public": "If off, only you can view the profile (headline still public).",
            "show_skills": "Allow recruiters to see your skills.",
            "show_education": "Allow recruiters to see your education.",
            "show_experience": "Allow recruiters to see your experience.",
            "show_links": "Allow recruiters to see your links (GitHub, LinkedIn, portfolio).",
        }
        widgets = {
            "skills": forms.Textarea(attrs={"rows": 3}),
            "education": forms.Textarea(attrs={"rows": 3}),
            "experience": forms.Textarea(attrs={"rows": 3}),
            "links": forms.Textarea(attrs={"rows": 2, "placeholder": "One per line"}),
        }
