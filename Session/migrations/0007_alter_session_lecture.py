# Generated by Django 4.2.7 on 2024-02-12 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manage', '0018_term_status'),
        ('Session', '0006_alter_session_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='lecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Manage.lecture'),
        ),
    ]
