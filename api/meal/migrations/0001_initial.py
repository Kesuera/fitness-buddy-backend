# Generated by Django 4.0.3 on 2022-03-30 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('desert', 'Desert')], max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('ingredients', models.CharField(max_length=100)),
                ('prep_time', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
                ('photo_path', models.FileField(null=True, upload_to='')),
                ('trainer_id', models.ForeignKey(db_column='trainer_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'meals',
            },
        ),
    ]
