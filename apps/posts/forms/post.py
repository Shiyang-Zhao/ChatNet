from django import forms
from ..models.post import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "file",
            "content",
            "is_published",
        ]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "file",
            "content",
            "is_published",
        ]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
