from django import forms
from ..models.chat import Chat


class PrivateChatCreateForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = []


class GroupChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["participants", "title", "description"]
