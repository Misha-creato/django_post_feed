from django.contrib import messages

from posts import check
from posts.models import Post


def update_or_create_post(request, action) -> (int, Post):
    data = request.POST
    files = request.FILES
    user = request.user
    if check.post_data(data=data):
        print(f'Создание или обновление поста {data} {files}')
        try:
            post, flag = Post.objects.update_or_create(
                slug=data.get('slug'),
                defaults={
                    'user': user,
                    'title': data['title'],
                    'description': data['description'],
                    'image': files.get('image'),
                },
            )
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
    messages.error(
        request=request,
        message='Заголовок является обязательным полем',
    )
    return 400, None


def find_post(request, slug) -> (int, Post):
    post = Post.objects.filter(slug=slug).first()
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