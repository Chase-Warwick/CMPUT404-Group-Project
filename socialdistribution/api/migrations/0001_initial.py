# Generated by Django 3.2.7 on 2021-10-20 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
from ..models import SiteSetting


def allow_user(apps, schema_editor):
    # automatically seed allow_user setting
    SiteSetting.objects.create_setting(setting="allow_join", on=True)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4,
                 primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('type', models.CharField(default='author', max_length=255)),
                ('host', models.URLField(
                    default='http://127.0.0.1:8000/api/', max_length=255)),
                ('displayName', models.CharField(max_length=255, unique=True)),
                ('url', models.CharField(
                    default='http://127.0.0.1:8000/api/', max_length=255)),
                ('github', models.CharField(blank=True,
                 max_length=50, null=True, unique=True)),
                ('email', models.EmailField(max_length=255,
                 unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['displayName'],
            },
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('setting', models.CharField(max_length=255, unique=True)),
                ('on', models.BooleanField()),
            ],
        ),
        migrations.RunPython(allow_user),  # seed db with allow_user setting
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('id', models.CharField(max_length=255,
                 primary_key=True, serialize=False, unique=True)),
                ('source', models.URLField(max_length=255)),
                ('origin', models.URLField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('content_type', models.CharField(choices=[('text/markdown', 'Markdown'), ('text/plain', 'Plain'), (
                    'application/base64', 'Application'), ('image/png;base64', 'Png'), ('image/jpg;base64', 'Jpg')], max_length=255)),
                ('text_content', models.TextField(blank=True)),
                ('image_content', models.ImageField(blank=True, upload_to='')),
                ('categories', models.TextField(blank=True)),
                ('count', models.IntegerField(default=0)),
                ('size', models.IntegerField()),
                ('comment_page', models.CharField(max_length=255)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(choices=[
                 ('public', 'Public')], default='public', max_length=255)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=255)),
                ('comment', models.TextField()),
                ('content_type', models.CharField(max_length=255)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.post')),
            ],
        ),
    ]
