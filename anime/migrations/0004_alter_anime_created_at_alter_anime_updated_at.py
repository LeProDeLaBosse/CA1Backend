# Generated by Django 4.1.7 on 2023-03-22 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0003_anime_created_at_anime_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 22, 20, 11, 49, 604516, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='anime',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 22, 20, 11, 49, 604516, tzinfo=datetime.timezone.utc)),
        ),
    ]
