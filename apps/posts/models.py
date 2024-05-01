from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images',
        verbose_name='Картинка',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
