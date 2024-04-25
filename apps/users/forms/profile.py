from django import forms
from ..models.profile import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_image", "location", "website", "birthday"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_image", "location", "website", "birthday"]