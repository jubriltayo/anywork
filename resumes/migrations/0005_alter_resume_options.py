# Generated by Django 5.1.6 on 2025-03-07 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0004_alter_resume_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resume',
            options={'ordering': ['-uploaded_at'], 'verbose_name_plural': 'Resumes'},
        ),
    ]
