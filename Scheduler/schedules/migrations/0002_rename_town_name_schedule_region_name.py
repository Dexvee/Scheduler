# Generated by Django 5.1.2 on 2024-11-15 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='town_name',
            new_name='region_name',
        ),
    ]