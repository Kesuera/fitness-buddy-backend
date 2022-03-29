# Generated by Django 4.0.3 on 2022-03-29 01:35

import api.meal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0003_remove_meal_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='photo_path',
        ),
        migrations.AddField(
            model_name='meal',
            name='image',
            field=models.ImageField(null=True, upload_to=api.meal.models.upload_location),
        ),
    ]
