# Generated by Django 5.1.6 on 2025-03-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('employer', 'Employer'), ('job_seeker', 'Job Seeker'), ('admin', 'Admin')], max_length=20),
        ),
    ]
