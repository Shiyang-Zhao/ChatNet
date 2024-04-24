from django import forms
from ..models.comment import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]
