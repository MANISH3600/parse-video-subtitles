# Generated by Django 3.2.25 on 2024-06-17 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_subtitle_date_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtitle',
            old_name='date_time',
            new_name='end_time',
        ),
    ]
