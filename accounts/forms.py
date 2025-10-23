# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, RecruiterProfile

User = get_user_model()

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

class RecruiterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = [
            'company_name', 'company_description', 'company_website', 'company_logo',
            'phone', 'address', 'industry', 'company_size'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'company_website': forms.URLInput(attrs={'class': 'form-control'}),
            'company_logo': forms.URLInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'company_size': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'company_name': 'Company Name',
            'company_description': 'Company Description',
            'company_website': 'Company Website',
            'company_logo': 'Company Logo URL',
            'phone': 'Phone Number',
            'address': 'Company Address',
            'industry': 'Industry',
            'company_size': 'Company Size',
        }
        help_texts = {
            'company_logo': 'URL to your company logo image',
            'company_size': 'e.g., 1-10, 11-50, 51-200, 201-500, 500+',
        }
