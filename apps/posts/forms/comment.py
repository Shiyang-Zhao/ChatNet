from django import forms
from ..models.comment import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "cols": 40,
                    "rows": 3,
                    "class": "form-control",
                    "style": "height: 40px;",
                }
            ),
        }


class ReplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "cols": 40,
                    "rows": 3,
                    "class": "form-control",
                    "style": "height: 40px;",
                }
            ),
        }
