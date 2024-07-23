from apps.posts.models.post import Post
from apps.users.forms.user import UserLoginForm, UserSignUpForm
from django.db.models import Case, When


def user_auth_forms(request):
    return {
        "user_login_form": UserLoginForm(),
        "user_signup_form": UserSignUpForm(),
    }


def recent_posts(request):
    recent_post_pks = request.session.get("recent_post_pks", [])
    if recent_post_pks:
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(recent_post_pks)]
        )
        recent_posts = Post.objects.filter(pk__in=recent_post_pks).order_by(
            preserved_order
        )
    else:
        recent_posts = Post.objects.none()
    return {
        "recent_posts": recent_posts,
    }
