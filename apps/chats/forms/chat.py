from django import forms
from ..models.chat import Chat
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError

User = get_user_model()


class PrivateChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = []


class GroupChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["participants"]
        widgets = {
            "participants": forms.SelectMultiple(attrs={"size": 10}),
        }

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("creator", None)
        super().__init__(*args, **kwargs)
        if self.creator:
            self.fields["participants"].queryset = User.objects.exclude(
                pk=self.creator.pk
            )

    def clean_participants(self):
        participants = self.cleaned_data.get("participants", User.objects.none())
        if self.creator and self.creator not in participants:
            participants |= User.objects.filter(pk=self.creator.pk)
        if len(participants) < 2:
            raise ValidationError("A group chat requires at least two participants")
        return participants
