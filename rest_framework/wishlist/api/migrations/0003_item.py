# Generated by Django 4.1.5 on 2023-01-24 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_wishlist_date_remove_wishlist_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.wishlist')),
            ],
        ),
    ]
