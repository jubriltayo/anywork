# Generated by Django 4.2.4 on 2023-08-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0002_professional_service_alter_professional_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='service',
            field=models.CharField(choices=[('tutorship', 'tutorship'), ('transportation', 'transportation'), ('food', 'food'), ('cleaning', 'cleaning')], max_length=64),
        ),
    ]
