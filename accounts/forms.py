from django import forms
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["headline","skills","education","experience","links","is_public","commute_radius_km"]