from apps.posts.models.post import Post
from apps.users.forms.user import UserLoginForm, UserSignUpForm


def user_auth_forms(request):
    return {
        "user_login_form": UserLoginForm(),
        "user_signup_form": UserSignUpForm(),
    }


def recent_posts(request):
    recent_post_ids = request.session.get("recent_posts", [])
    recent_posts = Post.objects.filter(id__in=recent_post_ids)
    return {
        "recent_posts": recent_posts,
    }
