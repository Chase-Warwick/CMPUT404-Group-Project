# Generated by Django 3.2.7 on 2021-10-16 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211015_2214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['displayName']},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='displayName',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
