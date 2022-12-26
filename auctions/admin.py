from django.contrib import admin
from auctions.models import AuctionBid, AuctionItem, Category, Watchlist, Comment

# Register your models here.


admin.site.register([AuctionItem, AuctionBid, Category, Watchlist, Comment])