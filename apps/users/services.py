import json
import os
import uuid

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash,
)
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
)

from django.core.mail import send_mail
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.db.utils import IntegrityError

from config.settings import (
    EMAIL_HOST_USER,
    SEND_EMAILS,
)
from posts.models import Post

from users import check
from users.models import CustomUser
from users.forms import (
    CustomUserCreationForm,
    LoginForm,
    PasswordResetRequestForm,
)


CUR_DIR = os.path.dirname(__file__)


def create_and_return_user(request, data) -> (int, CustomUser):
    try:
        user = CustomUser.objects.create_user(
            email=data['email'],
            username=data['username'],
            password=data['password1'],
        )
        messages.success(
            request=request,
            message='Вы успешно зарегистрировались'
        )
        return 200, user
    except Exception as exc:
        print(f'Не удалось создать пользователя {exc}')
        messages.error(
            request=request,
            message='Возникла ошибка при создании пользователя, пожалуйста, попробуйте позже'
        )
        return 500, None


def send_mail_to_user(request, user, action):
    url_hash = set_user_url_hash(user=user)
    url = request.build_absolute_uri(reverse(action, args=(url_hash,)))

    with open(f'{CUR_DIR}/mail_messages/{action}.json') as file:
        data = json.load(file)

    subject = data['subject']
    message = data['message'].format(url=url)

    if not SEND_EMAILS:
        print('Отправка писем отключена')
        return 203
    try:
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])
        messages.success(
            request=request,
            message=data['send_success'],
        )
    except Exception as exc:
        print(f'Произошла ошибка при отправке письма пользователю {exc}')
        messages.warning(
            request=request,
            message=data['send_failed'],
        )
        return 202
    return 200


def is_user_logged_in(request, data) -> int:
    user = authenticate(
        request=request,
        username=data['email'],
        password=data['password'],
    )
    if user is None:
        messages.error(
            request=request,
            message='Неправильные адрес электронной почты или пароль',
        )
        return 401
    login(
        request=request,
        user=user,
    )
    return 200


def set_form_error_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(
                request=request,
                message=error
            )


def set_user_url_hash(user):
    url_hash = str(uuid.uuid4())
    user.url_hash = url_hash
    user.save()
    return url_hash


def register_user(request) -> int:
    data = request.POST
    form = CustomUserCreationForm(data)
    if not form.is_valid():
        set_form_error_messages(
            request=request,
            form=form,
        )
        return 400
    status, user = create_and_return_user(
        request=request,
        data=data,
    )
    if status == 200:
        email_send_status = send_mail_to_user(
            request=request,
            user=user,
            action='confirm_email',
        )
        if email_send_status == 200:
            user.mail_sent = True
            user.save()
    return status


def login_user(request) -> int:
    data = request.POST
    form = LoginForm(data)
    if not form.is_valid():
        set_form_error_messages(
            request=request,
            form=form,
        )
        return 400
    return is_user_logged_in(request=request, data=data)


def confirm_email(request, url_hash) -> int:
    try:
        user = CustomUser.objects.filter(url_hash=url_hash).first()
    except Exception as exc:
        print(exc)
        messages.error(
            request=request,
            message='Возникла ошибка на стороне сервера',
        )
        return 500
    if user is None:
        messages.error(
            request=request,
            message='Неверный токен',
        )
        return 404
    user.email_confirmed = True
    user.url_hash = None
    user.save()
    messages.success(
        request=request,
        message='Адрес электронной почты успешно подтвержден',
    )
    return 200


def settings_user(request) -> int:
    user = request.user
    data = request.POST
    form = PasswordChangeForm(user, data)
    if not form.is_valid():
        set_form_error_messages(
            request=request,
            form=form,
        )
        return 400
    form.save()
    messages.success(
        request=request,
        message='Пароль успешно изменен',
    )
    update_session_auth_hash(
        request=request,
        user=user,
    )
    return 200


def password_reset_request(request) -> int:
    data = request.POST
    form = PasswordResetRequestForm(data)
    if not form.is_valid():
        set_form_error_messages(
            request=request,
            form=form,
        )
        return 400
    email = form.cleaned_data['email']
    try:
        user = CustomUser.objects.filter(email=email).first()
    except Exception as exc:
        print(exc)
        messages.error(
            request=request,
            message='Возникла ошибка на стороне сервера',
        )
        return 500
    if user is None:
        messages.error(
            request=request,
            message=f'Пользователь с адресом электронной почты {email} не найден',
        )
        return 404
    send_mail_to_user(
        request=request,
        user=user,
        action='password_reset',
    )
    return 200


def password_reset_get(request, url_hash) -> int:
    try:
        user = CustomUser.objects.filter(url_hash=url_hash).first()
    except Exception as exc:
        print(exc)
        messages.error(
            request=request,
            message='Возникла ошибка на стороне сервера',
        )
        return 500
    if user is None:
        messages.error(
            request=request,
            message='Неверный токен',
        )
        return 404
    return 200


def password_reset_post(request, url_hash):
    try:
        user = CustomUser.objects.filter(url_hash=url_hash).first()
    except Exception as exc:
        print(exc)
        messages.error(
            request=request,
            message='Возникла ошибка на стороне сервера',
        )
        return 500
    if user is None:
        messages.error(
            request=request,
            message='Неверный токен',
        )
        return 404
    data = request.POST
    form = SetPasswordForm(user, data)
    if not form.is_valid():
        set_form_error_messages(
            request=request,
            form=form,
        )
        return 400
    form.user.url_hash = None
    form.save()
    messages.success(
        request=request,
        message='Пароль успешно изменен',
    )
    return 200


def get_user(request, username) -> (int, CustomUser):
    try:
        user = (CustomUser.objects.filter(username=username).
                prefetch_related(Prefetch('posts',
                                          queryset=Post.objects.filter(~Q(hide_from_users=request.user)))).
                first())
    except Exception as exc:
        print(f'Возникла ошибка на стороне сервера {exc}')
        return 500, None
    if user is None:
        messages.error(
            request=request,
            message=f'Пользователь с логином {username} не найден',
        )
        return 404, None
    return 200, user


def profile_post(request, username) -> (int, CustomUser):
    status, user = get_user(
        request=request,
        username=username,
    )
    if status != 200:
        return status
    data = request.POST
    files = request.FILES
    if not check.profile_data(data=data):
        messages.error(
            request=request,
            message='Логин является обязательным полем',
        )
        return 400
    user.avatar = files.get('avatar', user.avatar)
    user.username = data.get('username', user.username)
    user.profile_description = data.get('profile_description', user.profile_description)
    try:
        user.save()
        messages.success(
            request=request,
            message='Профиль успешно обновлен',
        )
        return 200
    except IntegrityError as exc:
        print(exc)
        messages.error(
            request=request,
            message=f'Логин {data["username"]} уже существует',
        )
    except Exception as exc:
        print(f'Возникла ошибка при обновлении профиля {exc}')
    return 400


