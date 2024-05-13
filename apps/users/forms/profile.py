from django import forms
from ..models.profile import Profile
from PIL import Image
import tempfile
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_image", "location", "website", "birthday"]

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")
        if image:
            img = Image.open(image)
            img.thumbnail(
                (800, 800), Image.Resampling.LANCZOS
            )  # Resize to reduce dimensions

            output = BytesIO()
            # Set a fixed quality of 70
            img.save(output, format="JPEG", quality=70)
            output.seek(0)

            new_image = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{image.name.split('.')[0]}_compressed.jpg",
                "image/jpeg",
                output.tell(),
                None,
            )
            return new_image

        return image

    # def save(self, commit=True):
    #     profile = super(ProfileUpdateForm, self).save(commit=False)
    #     if commit:
    #         profile.save()
    #     return profile
