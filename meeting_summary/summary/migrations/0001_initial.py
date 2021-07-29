# Generated by Django 3.1.13 on 2021-07-27 17:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Caption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start', models.CharField(max_length=255, verbose_name='Start time')),
                ('end', models.CharField(max_length=255, verbose_name='End time')),
                ('name', models.CharField(max_length=255, verbose_name='User Name')),
                ('text', models.TextField(verbose_name='Text')),
                ('word_count', models.PositiveSmallIntegerField(verbose_name='Word Count')),
                ('transcript', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='summary.meeting')),
            ],
        ),
    ]