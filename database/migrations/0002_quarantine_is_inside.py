# Generated by Django 3.2.7 on 2022-02-08 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quarantine',
            name='is_inside',
            field=models.BooleanField(default=True),
        ),
    ]
