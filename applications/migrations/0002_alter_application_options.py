# Generated by Django 5.1.6 on 2025-03-06 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['application_id'], 'verbose_name_plural': 'Applications'},
        ),
    ]
