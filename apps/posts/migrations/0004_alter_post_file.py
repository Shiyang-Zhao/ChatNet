# Generated by Django 5.0.4 on 2024-05-10 10:07

import apps.posts.models.post
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=apps.posts.models.post.post_file_directory_path),
        ),
    ]
