# Generated by Django 5.1.6 on 2025-03-07 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_alter_skill_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='JobSeekerSkill',
        ),
    ]
