import uuid

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class AuctionCategory(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Auction Categories'


class AuctionItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    description = models.TextField()
    category = models.ForeignKey(AuctionCategory, on_delete=models.CASCADE, null=True, default=None,
                                 related_name='auction_items')
    image = models.ImageField(null=True, default='default.jpg')
    image_url = models.URLField(max_length=500, null=True, blank=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='items')
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(1)], default=0)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(1)], default=0)
    watchlist = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return str(self.title)


class AuctionBid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, null=True, related_name='auction_bid')
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_bid')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.auction_item} = {self.bid}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.auction_item} - {self.author}"
