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

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.")
        return content

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

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.")
        return content