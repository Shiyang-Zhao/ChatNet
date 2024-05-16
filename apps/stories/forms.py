from django import forms
from .models import Story


class StoryCreateForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["file", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "file": forms.FileInput(
                attrs={"accept": "image/*,video/*", "class": "form-control"}
            ),
        }


class StoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["file", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "file": forms.FileInput(
                attrs={"accept": "image/*,video/*", "class": "form-control"}
            ),
        }
