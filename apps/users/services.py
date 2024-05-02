import json
import os
import uuid

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    update_session_auth_hash,
)

from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
)

from config.settings import (
    EMAIL_HOST_USER,
    SEND_EMAILS,
)

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
    url_hash = get_user_url_hash(user=user)
    url = request.build_absolute_uri(reverse(action, args=(url_hash,)))

    with open(f'{CUR_DIR}/mail_messages/{action}.json') as file:
        data = json.load(file)

    subject = data['subject']
    message = data['message'].format(url=url)

    if SEND_EMAILS:
        try:
            send_mail(subject, message, EMAIL_HOST_USER, [user.email])
        except Exception as exc:
            print('Произошла ошибка при отправке пользователя')
    else:
        print('Отправка писем отключена')


def is_user_logged_in(request, data) -> int:
    user = authenticate(
        request=request,
        username=data['email'],
        password=data['password'],
    )
    if user is not None:
        login(
            request=request,
            user=user,
        )
        return 200
    messages.error(
        request=request,
        message='Неправильные адрес электронной почты или пароль',
    )
    return 401


def set_form_error_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(
                request=request,
                message=error
            )


def get_user_url_hash(user):
    url_hash = str(uuid.uuid4())
    user.url_hash = url_hash
    user.save()
    return url_hash


def register_user(request) -> int:
    data = request.POST
    form = CustomUserCreationForm(data)
    if form.is_valid():
        status, user = create_and_return_user(
            request=request,
            data=data,
        )
        if status == 200:
            send_mail_to_user(
                request=request,
                user=user,
                action='confirm_email',
            )
        return status
    set_form_error_messages(
        request=request,
        form=form,
    )
    return 400


def login_user(request) -> int:
    data = request.POST
    form = LoginForm(data)
    if form.is_valid():
        return is_user_logged_in(request=request, data=data)
    set_form_error_messages(
        request=request,
        form=form,
    )
    return 400


def confirm_email(request, user):
    if user is not None:
        user.email_confirmed = True
        user.url_hash = None
        user.save()
        messages.success(
            request=request,
            message='Адрес электронной почты успешно подтвержден',
        )
    else:
        messages.error(
            request=request,
            message='Неверный токен',
        )


def settings_user(request) -> int:
    user = request.user
    data = request.POST
    form = PasswordChangeForm(user, data)
    if form.is_valid():
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
    set_form_error_messages(
        request=request,
        form=form,
    )
    return 400


def password_reset_request(request) -> int:
    data = request.POST
    form = PasswordResetRequestForm(data)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            send_mail_to_user(
                request=request,
                user=user,
                action='password_reset',
            )
            messages.success(
                request=request,
                message='Письмо для сброса пароля отправлено. '
                        'Проверьте свой почтовый ящик.',
            )
            return 200
        set_form_error_messages(
            request=request,
            form=form,
        )
    else:
        set_form_error_messages(
            request=request,
            form=form,
        )
    return 400


def password_reset_get(request, user) -> int:
    if user is not None:
        return 200
    messages.error(
        request=request,
        message='Неверный токен',
    )
    return 400


def password_reset_post(request, user):
    data = request.POST
    form = SetPasswordForm(user, data)
    if form.is_valid():
        form.user.url_hash = None
        form.save()
        messages.success(
            request=request,
            message='Пароль успешно изменен',
        )
        return 200
    set_form_error_messages(
        request=request,
        form=form,
    )
    return 400
