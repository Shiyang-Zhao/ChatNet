from django import forms
from ..models.comment import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]
        widgets = {
            "content": forms.Textarea(
                attrs={"cols": 40, "rows": 4, "class": "form-control"}
            ),
            "attachments": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]
        widgets = {
            "content": forms.Textarea(
                attrs={"cols": 40, "rows": 4, "class": "form-control"}
            ),
            "attachments": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
        }
