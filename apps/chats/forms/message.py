from django import forms
from ..models.message import Message


class MessageCreateForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 40,
                "placeholder": "Enter your message here",
                "class": "form-control",  # Adding Bootstrap class for styling
            }
        ),
        required=True,
        max_length=500,  # Enforcing max_length at the form level
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label="Attachments",
        help_text="Attach files. You can select multiple files.",  # Added help text directly in the field
    )

    class Meta:
        model = Message
        fields = ["content", "attachment"]
        help_texts = {
            "content": "You can enter up to 500 characters.",
        }
        error_messages = {
            "content": {
                "required": "Message content is required.",
                "max_length": "Message content cannot exceed 500 characters.",  # Corrected the error message key
            },
        }

    # def clean_content(self):
    #     content = self.cleaned_data.get("content")
    #     if any(word in content.lower() for word in ["forbidden", "restricted"]):  # Example: filtering specific words
    #         raise forms.ValidationError("Your message contains forbidden words.")
    #     return content
