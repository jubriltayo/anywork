# Generated by Django 5.1.6 on 2025-03-09 09:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cover_letter', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected'), ('accepted', 'Accepted')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Applications',
                'ordering': ['-applied_at'],
            },
        ),
    ]
