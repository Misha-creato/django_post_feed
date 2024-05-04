from django.db.models import Q

from posts.models import Post


def get_posts(request):
    try:
        posts = Post.objects.filter(~Q(hide_from_users=request.user))
        return 200, posts
    except Exception as exc:
        print(exc)
        return 500, None
