# Generated by Django 5.0.4 on 2024-06-17 07:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_saved_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='saved_by',
            field=models.ManyToManyField(blank=True, related_name='saved_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
