from django import forms
from .models import Job

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'location', 'latitude', 'longitude',
            'salary_min', 'salary_max', 'is_remote', 'visa_sponsorship',
            'company_name', 'company_logo'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Senior Software Engineer'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Describe the role, responsibilities, and requirements...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., San Francisco, CA'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'e.g., 37.7749'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'e.g., -122.4194'
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 80000'
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 120000'
            }),
            'is_remote': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'visa_sponsorship': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Tech Corp Inc.'
            }),
            'company_logo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/logo.png'
            }),
        }
        labels = {
            'title': 'Job Title',
            'description': 'Job Description',
            'location': 'Location',
            'latitude': 'Latitude (optional)',
            'longitude': 'Longitude (optional)',
            'salary_min': 'Minimum Salary',
            'salary_max': 'Maximum Salary',
            'is_remote': 'Remote Work Available',
            'visa_sponsorship': 'Visa Sponsorship Available',
            'company_name': 'Company Name',
            'company_logo': 'Company Logo URL',
        }
        help_texts = {
            'latitude': 'Optional: Used for location-based job matching',
            'longitude': 'Optional: Used for location-based job matching',
            'company_logo': 'Optional: URL to your company logo image',
        }

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        
        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        
        return cleaned_data

