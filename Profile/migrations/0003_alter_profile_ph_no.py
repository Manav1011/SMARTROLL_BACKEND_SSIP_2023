# Generated by Django 4.2.7 on 2023-11-16 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ph_no',
            field=models.CharField(max_length=20),
        ),
    ]
