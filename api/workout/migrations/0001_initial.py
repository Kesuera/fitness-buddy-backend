# Generated by Django 4.0.3 on 2022-04-07 12:20

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
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('full_body', 'Full Body'), ('lower_body', 'Lower Body'), ('upper_body', 'Upper Body'), ('condition', 'Condition')], max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('exercises', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
                ('trainer_id', models.ForeignKey(db_column='trainer_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'workouts',
            },
        ),
    ]
