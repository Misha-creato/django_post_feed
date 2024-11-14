from django.contrib import messages
from django.db.models import Q

from posts import check
from posts.models import Post


def update_or_create_post(request, action, slug=None) -> (int, Post):
    data = request.POST
    files = request.FILES
    user = request.user
    if not check.post_data(data=data):
        messages.error(
            request=request,
            message='Заголовок является обязательным полем',
        )
        return 400, None
    print(f'Создание или обновление поста {data} {files}')
    try:
        post = Post.objects.update_or_create(
            slug=slug,
            defaults={
                'slug': slug,
                'user': user,
                'image': files.get('image'),
                'title': data['title'],
                'description': data['description'],
                'hide': bool(data.get('hide')),
            },
        )[0]
        messages.success(
            request=request,
            message=f'Пост успешно {action}',
        )
        return 200, post
    except Exception as exc:
        print(f'Возникла ошибка {exc}')
        messages.error(
            request=request,
            message='Возникла ошибка. Попробуйте еще раз',
        )
        return 500, None


def get_post(request, slug, detail=False) -> (int, Post):
    if detail:
        post = Post.objects.filter(
            ~Q(hide_from_users=request.user),
            slug=slug,
        ).first()
    else:
        post = Post.objects.filter(
            slug=slug,
            user=request.user,
        ).first()
    if post is not None:
        return 200, post
    messages.error(
        request=request,
        message='Пост не найден',
    )
    return 404, None


def delete_post(request, post):
    post.delete()
    messages.success(
        request=request,
        message='Пост успешно удален',
    )


def search_posts(request):
    query = request.GET.get('search')
    try:
        posts = Post.objects.filter(
            ~Q(hide_from_users=request.user), title__icontains=query)
    except Exception as exc:
        print(exc)
        return 500, None
    if not posts.exists():
        return 404, None
    return 200, posts


def hide_post(request, slug):
    status, post = get_post(
        request=request,
        slug=slug,
        detail=True,
    )
    if status != 200:
        return status
    if check.post_author(request=request, post=post):
        messages.warning(
            request=request,
            message='Вы не можете скрыть свой пост',
        )
        return 403
    try:
        post.hide_from_users.add(request.user.id)
    except Exception as exc:
        print(f'Не удалось скрыть пост {exc}')
        messages.error(
            request=request,
            message='Не удалось скрыть пост. Ошибка на стороне сервера.'
        )
        return 500
    return 200