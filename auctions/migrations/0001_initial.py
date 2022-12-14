# Generated by Django 4.1.4 on 2022-12-20 10:53

import uuid

import autoslug.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionBid',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('bid', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True,
                                            validators=[django.core.validators.MinValueValidator(1)])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Auction Bid',
                'verbose_name_plural': 'Auction Bids',
                'ordering': ['-created', 'item'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug',
                 autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='AuctionItem',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug',
                 autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', unique=True)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='')),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True,
                                              validators=[django.core.validators.MinValueValidator(1)])),
                ('starting_bid', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True,
                                                     validators=[django.core.validators.MinValueValidator(1)])),
                ('watchlist', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='items', to='auctions.category')),
            ],
            options={
                'verbose_name': 'Auction Item',
                'verbose_name_plural': 'Auction Items',
                'ordering': ['-created', 'name'],
            },
        ),
    ]
