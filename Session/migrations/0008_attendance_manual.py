# Generated by Django 4.2.7 on 2024-02-24 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0007_alter_session_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='manual',
            field=models.BooleanField(default=False),
        ),
    ]
