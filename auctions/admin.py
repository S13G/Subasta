from django.contrib import admin

# Register your models here.
from auctions.models import AuctionBid, AuctionCategory, AuctionItem, Comment, User

admin.site.register([User, AuctionCategory, AuctionItem, AuctionBid, Comment])