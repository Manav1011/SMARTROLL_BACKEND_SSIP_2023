# Generated by Django 4.2.7 on 2023-11-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0007_alter_branch_branch_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='end_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='start_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
