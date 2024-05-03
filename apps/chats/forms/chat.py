from django import forms
from ..models.chat import Chat
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect


User = get_user_model()


class PrivateChatCreateForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = []


class GroupChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["participants", "title", "description"]

    # def __init__(self, *args, **kwargs):
    #     creator = kwargs.pop("creator", None)
    #     super(GroupChatCreateForm, self).__init__(*args, **kwargs)
    #     if creator is not None:
    #         self.fields["participants"].queryset = creator.profile.following.all()
