# Generated by Django 4.2.7 on 2023-12-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=255)),
                ('start_year', models.CharField(blank=True, max_length=4, null=True)),
                ('end_year', models.CharField(blank=True, max_length=4, null=True)),
                ('active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('branch_code', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=255)),
                ('code', models.IntegerField(unique=True)),
                ('credit', models.IntegerField()),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('subjects', models.ManyToManyField(blank=True, to='Manage.subject')),
            ],
        ),
    ]
