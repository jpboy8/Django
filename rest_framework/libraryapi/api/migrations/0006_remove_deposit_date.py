# Generated by Django 4.1.5 on 2023-01-23 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_deposit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='date',
        ),
    ]
