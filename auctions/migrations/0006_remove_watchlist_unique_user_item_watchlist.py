# Generated by Django 4.1.4 on 2022-12-22 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist_unique_user_item_watchlist'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='watchlist',
            name='unique_user_item_watchlist',
        ),
    ]