# Generated by Django 3.2.8 on 2021-11-29 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20211125_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]