# Generated by Django 4.0.3 on 2022-03-28 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0002_alter_meal_photo_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='duration',
        ),
    ]
