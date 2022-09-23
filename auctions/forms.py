from django import forms
from django.core.validators import MinValueValidator

from auctions.models import AuctionItem


class CreateForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['item_name', 'image', 'image_url', 'category', 'description', 'watchlist', 'price', 'starting_bid']