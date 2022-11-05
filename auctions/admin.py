from django.contrib import admin

# Register your models here.
from auctions.models import AuctionBid, AuctionCategory, AuctionItem, Comment

admin.site.register([AuctionCategory, AuctionItem, AuctionBid, Comment])