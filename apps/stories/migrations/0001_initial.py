# Generated by Django 5.0.4 on 2024-05-29 07:19

import apps.stories.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.stories.models.story_file_directory_path)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_expired', models.DateTimeField(default=apps.stories.models.default_expiration_date)),
                ('content', models.TextField(blank=True, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_stories', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, related_name='viewed_stories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
