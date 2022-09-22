from django.contrib import admin

# Register your models here.
from auctions.models import AuctionBid, AuctionCategory, AuctionItem, Comment, ItemImage, User

admin.site.register([User, ItemImage, AuctionCategory, AuctionItem, AuctionBid, Comment])