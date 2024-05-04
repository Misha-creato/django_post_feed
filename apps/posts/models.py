import hashlib

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    hide_from_users = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='hidden_posts',
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
    slug = models.SlugField(
        unique=True,
        verbose_name='URL',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.image:
            if self.pk:
                post = Post.objects.get(pk=self.pk)
                self.image = post.image
        slug_title = slugify(self.title)
        hash_id = hashlib.sha256(str(self.id).encode()).hexdigest()[:12]
        self.slug = f'{slug_title}#{hash_id}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
