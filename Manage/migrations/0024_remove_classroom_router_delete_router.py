# Generated by Django 4.2.7 on 2024-02-24 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0023_lecture_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='router',
        ),
        migrations.DeleteModel(
            name='Router',
        ),
    ]
