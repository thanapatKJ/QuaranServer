# Generated by Django 3.2.7 on 2022-02-11 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_quarantine_is_inside'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facedata',
            name='data',
        ),
        migrations.AddField(
            model_name='facedata',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
