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
