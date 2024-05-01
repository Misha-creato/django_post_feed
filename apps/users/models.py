import io
from PIL import Image

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):
        username = email.split('@')[0]
        return self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Логин',
    )
    profile_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание профиля',
    )
    avatar = models.ImageField(
        default='avatars/default.jpg',
        upload_to='avatars',
        verbose_name='Аватар',
    )
    thumbnail = models.ImageField(
        default='thumbnails/default.jpg',
        upload_to='thumbnails',
        verbose_name='Миниатюра аватара',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Статус суперпользователя',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус персонала',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
    )
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Адрес электронной почты подтвержден',
    )
    url_hash = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Хэш',
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.pk and self.avatar:
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar
            if self.avatar != old_avatar:
                self.__make_thumbnail()
        super().save(*args, **kwargs)

    def __make_thumbnail(self):
        with self.avatar as avatar_img:
            img = Image.open(avatar_img)

            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')

            thumbnail_size = (100, 100)

            img.thumbnail(thumbnail_size)

            temp_thumb = io.BytesIO()
            img.save(temp_thumb, format='JPEG')

            self.thumbnail = SimpleUploadedFile(self.avatar.name, temp_thumb.getvalue())

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
