# Generated by Django 4.2.7 on 2024-02-24 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0010_attendance_latt_attendance_long_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='marking_ip',
        ),
    ]
