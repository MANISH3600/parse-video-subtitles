# Generated by Django 3.2.25 on 2024-06-17 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitle',
            name='date_time',
            field=models.FloatField(null=True),
        ),
    ]
