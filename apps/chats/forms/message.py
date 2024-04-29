from django import forms
from ..models.message import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "content",
            "attachment"
        ]

    # content = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "rows": 4,
    #             "cols": 40,
    #             "placeholder": "Enter your message here",
    #             "class": "form-control",  # Adding Bootstrap class for styling
    #         }
    #     ),
    #     required=True,
    #     max_length=500,
    # )

    # class Meta:
    #     model = Message
    #     fields = ["content"]
    #     help_texts = {
    #         "content": "You can enter up to 500 characters.",
    #     }
    #     error_messages = {
    #         "content": {
    #             "required": "Message content is required.",
    #             "max_length": "Message content cannot exceed 500 characters.",  # Corrected the error message key
    #         },
    #     }
