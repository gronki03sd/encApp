# Generated by Django 5.1.7 on 2025-05-10 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_profile_old_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='old_cart',
            field=models.TextField(blank=True, null=True),
        ),
    ]
