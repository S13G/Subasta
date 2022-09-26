# Generated by Django 4.1.1 on 2022-09-26 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionbid_bidder_alter_auctionitem_listed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionbid',
            name='auction_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s', to='auctions.auctionitem'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='auction_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionitem'),
        ),
    ]
