# Generated by Django 5.1.6 on 2025-03-07 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_alter_application_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['applied_at'], 'verbose_name_plural': 'Applications'},
        ),
    ]
