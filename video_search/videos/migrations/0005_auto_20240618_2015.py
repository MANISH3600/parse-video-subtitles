# Generated by Django 3.2.25 on 2024-06-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20240618_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='s3_key',
        ),
        migrations.AddField(
            model_name='video',
            name='local_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
