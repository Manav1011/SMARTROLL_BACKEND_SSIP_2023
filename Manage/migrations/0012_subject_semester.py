# Generated by Django 4.2.7 on 2024-02-08 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0011_alter_semester_end_year_alter_semester_start_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.semester'),
        ),
    ]
