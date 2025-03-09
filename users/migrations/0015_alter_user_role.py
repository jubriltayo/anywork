# Generated by Django 5.1.6 on 2025-03-07 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('job_seeker', 'Job Seeker'), ('employer', 'Employer')], max_length=20),
        ),
    ]
