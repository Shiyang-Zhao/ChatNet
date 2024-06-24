from apps.users.forms.user import UserLoginForm, UserSignUpForm


def user_auth_forms(request):
    return {
        "user_login_form": UserLoginForm(),
        "user_signup_form": UserSignUpForm(),
    }
