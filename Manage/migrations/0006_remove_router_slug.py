# Generated by Django 4.2.7 on 2024-02-07 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0005_classroom_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='router',
            name='slug',
        ),
    ]
