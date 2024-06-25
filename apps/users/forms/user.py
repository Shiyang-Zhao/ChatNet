from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "autocomplete": "username"}
        )
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Email", "autocomplete": "email"}
        )
        self.fields["password1"].label = ""
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Password", "autocomplete": "new-password"}
        )
        self.fields["password2"].label = ""
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password", "autocomplete": "new-password"}
        )


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember me")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Username", "autocomplete": "username"}
        )
        self.fields["password"].label = ""
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Password", "autocomplete": "current-password"}
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
