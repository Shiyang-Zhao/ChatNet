from django import forms
from ..models.message import Message


class MessageCreationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content", "attachment"]
