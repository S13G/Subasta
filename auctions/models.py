import uuid

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models, IntegrityError

from users.models import User


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from="name", always_update=True, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)


class AuctionItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from="name", always_update=True, unique=True)
    image = models.ImageField(null=True, blank=True, default='default.jpg')
    image_link = models.URLField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None, related_name="items")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)], null=True,
                                default=0)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)], default=0,
                                       null=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="item")
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auction Item"
        verbose_name_plural = "Auction Items"
        ordering = ["-created"]

    def __str__(self):
        return str(self.name)

    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def auction_item_bidders(self):
        queryset = self.bids.all().values_list("bidder_id", flat=True)
        return queryset

    @property
    def commenters(self):
        queryset = self.comments.all().values_list("owner_id", flat=True)
        return queryset


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="watchlists")
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, null=True)

    class Meta:
        # to make sure 2 exact objects don't exist
        constraints = [
            models.UniqueConstraint(fields=["user", "item"], name="unique_user_item_watchlist")
        ]

    def __str__(self):
        return f"{self.user} -- {self.item}"


class AuctionBid(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    item = models.ForeignKey(AuctionItem, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name='bidded_item', on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)], default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auction Bid"
        verbose_name_plural = "Auction Bids"
        ordering = ["created"]

    def __str__(self):
        return f"{self.bidder} - {self.item} - {self.bid}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    item = models.ForeignKey(AuctionItem, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # to make sure 2 exact objects don't exist
        constraints = [
            models.UniqueConstraint(fields=["owner", "item"], name="unique_user_item_comment")
        ]

    def __str__(self):
        return f"{self.owner} - {self.item}"
