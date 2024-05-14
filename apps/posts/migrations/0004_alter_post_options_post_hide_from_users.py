# Generated by Django 4.2 on 2024-05-04 11:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_alter_post_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AddField(
            model_name='post',
            name='hide_from_users',
            field=models.ManyToManyField(blank=True, related_name='hidden_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]