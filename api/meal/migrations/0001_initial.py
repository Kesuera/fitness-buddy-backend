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
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('desert', 'Desert')], max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('ingredients', models.CharField(max_length=100)),
                ('prep_time', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
                ('photo_path', models.FilePathField(unique=True)),
                ('trainer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'meals',
            },
        ),
    ]