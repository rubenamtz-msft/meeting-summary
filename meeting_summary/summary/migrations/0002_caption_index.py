# Generated by Django 3.1.13 on 2021-07-27 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caption',
            name='index',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Index'),
        ),
    ]
