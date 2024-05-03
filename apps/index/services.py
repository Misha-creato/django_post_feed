from posts.models import Post


def get_posts():
    try:
        posts = Post.objects.all()
        return 200, posts
    except Exception as exc:
        print(exc)
        return 500, None
