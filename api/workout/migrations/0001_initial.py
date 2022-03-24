# Generated by Django 4.0.2 on 2022-03-24 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
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
                ('trainer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'workouts',
            },
        ),
    ]
