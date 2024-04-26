from django import forms
from ..models.chat import Chat


class PrivateChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        exclude = ()

    def save(self, commit=True):
        chat = super().save(commit=False)
        participants = [self.request.user, self.kwargs["second_user"]]
        chat.title = f"{participants[0].username} & {participants[1].username}"
        chat.chat_type = Chat.PRIVATE
        chat.description = ""

        if commit:
            chat.save()
            chat.participants.set(participants)
        return chat


class GroupChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = [
            "participants",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.chat_type = Chat.GROUP
