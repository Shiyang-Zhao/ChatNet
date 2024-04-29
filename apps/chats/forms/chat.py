from django import forms
from ..models.chat import Chat


class PrivateChatCreateForm(forms.ModelForm):
    
    class Meta:
        model = Chat
        fields = []


class GroupChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = [
            "participants",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.chat_type = Chat.GROUP
