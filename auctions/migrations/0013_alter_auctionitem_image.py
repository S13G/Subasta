# Generated by Django 4.1.4 on 2022-12-31 19:05

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_comment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='items'),
        ),
    ]