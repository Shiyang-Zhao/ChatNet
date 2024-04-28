from django import forms
from ..models.comment import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "attachments", "visibility"]
