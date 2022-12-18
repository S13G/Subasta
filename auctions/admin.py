from django.contrib import admin
from auctions.models import AuctionBid, AuctionItem, Category

# Register your models here.


admin.site.register([AuctionItem, AuctionBid, Category])