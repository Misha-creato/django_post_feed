# Generated by Django 4.2 on 2024-05-03 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mail_sent',
            field=models.BooleanField(default=False, verbose_name='Письмо для подтверждения отправлено'),
        ),
    ]
