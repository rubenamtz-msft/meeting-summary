# Generated by Django 3.1.13 on 2021-07-27 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0002_caption_index'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caption',
            old_name='transcript',
            new_name='meeting',
        ),
    ]
