from django.contrib import messages

from posts import check
from posts.models import Post


def create_post(request, user, data, files):
    if check.post_data(data=data):
        print(f'Создание поста {data} {files}')
        try:
            post = Post.objects.create(
                user=user,
                title=data['title'],
                description=data['description'],
                image=files.get('image'),
            )
            messages.success(
                request=request,
                message='Пост успешно создан',
            )
            return 200, post
        except Exception as exc:
            print(f'Возникла ошибка при создании поста {exc}')
            messages.error(
                request=request,
                message='Возникла ошибка при создании поста. Попробуйте еще раз',
            )
    else:
        messages.error(
            request=request,
            message='Заголовок является обязательным полем',
        )
    return 400, None


def update_post(request, post, data, files):
    if check.post_data(data=data):
        print(f'Обновление поста {post}')


def update_post_request(request, post, data, files):
    if post is not None:
        data = request.POST
        files = request.FILES
        return update_post(
            request=request,
            post=post,
            data=data,
            files=files,
        )
    messages.error(
        request=request,
        message='Пост не найден'
    )
    return 404, None