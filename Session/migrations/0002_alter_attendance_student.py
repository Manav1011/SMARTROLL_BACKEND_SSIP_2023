# Generated by Django 4.2.7 on 2024-02-10 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StakeHolders', '0002_student_sr_no'),
        ('Session', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='StakeHolders.student'),
        ),
    ]
