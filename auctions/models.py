from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from auctions.item import get_media_paths


class User(AbstractUser):
    pass


class ItemImage(models.Model):
    image = models.ImageField(upload_to=get_media_paths)


class AuctionCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Auction Category'
        verbose_name_plural = 'Auction Categories'

    def __str__(self) -> str:
        return f"{self.name}"
    

class AuctionItem(models.Model):
    item_name = models.CharField(max_length=255)
    image = models.ForeignKey(ItemImage, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    watchlist = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    listed_by = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.item_name}"


class AuctionBid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    bidder = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.bidder} = {self.bid}"


class Comment(models.Model):
    comment = models.TextField()
    author = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.comment}"