from django import forms
from ..models.chat import Chat


class ChatCreationForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["title", "description", "participants", "image"]
