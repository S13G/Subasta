from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

import uuid


class User(AbstractUser):
    pass


class AuctionCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Auction Category'
        verbose_name_plural = 'Auction Categories'

    def __str__(self) -> str:
        return f"{self.name}"
    

class AuctionItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    item_name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, default='default.jpg')
    image_url = models.URLField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(AuctionCategory, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    watchlist = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    listed_by = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.item_name}"


class AuctionBid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    bidder = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.bidder} = {self.bid}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.auction_item} - {self.author}"