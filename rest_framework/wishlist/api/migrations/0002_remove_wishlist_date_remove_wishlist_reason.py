# Generated by Django 4.1.5 on 2023-01-24 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='date',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='reason',
        ),
    ]
