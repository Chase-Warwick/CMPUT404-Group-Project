# Generated by Django 3.2.7 on 2021-10-17 06:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_update_user_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]
