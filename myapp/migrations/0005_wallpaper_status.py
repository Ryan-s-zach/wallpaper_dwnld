# Generated by Django 4.2.5 on 2023-12-03 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_wallpaper'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpaper',
            name='status',
            field=models.BooleanField(default=False, help_text='0-show,1-hidden'),
        ),
    ]
