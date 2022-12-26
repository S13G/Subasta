# Generated by Django 4.1.4 on 2022-12-26 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0008_alter_auctionbid_options_auctionitem_closed_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auctionbid',
            options={'ordering': ['created'], 'verbose_name': 'Auction Bid', 'verbose_name_plural': 'Auction Bids'},
        ),
        migrations.AlterModelOptions(
            name='auctionitem',
            options={'ordering': ['-created'], 'verbose_name': 'Auction Item', 'verbose_name_plural': 'Auction Items'},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionitem')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
