from django import forms
from django.core.validators import MinValueValidator

from auctions.models import AuctionItem


class CreateForm(forms.ModelForm):
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])

    class Meta:
        model = AuctionItem
        fields = ['item_name', 'image', 'image_url', 'category', 'description', 'watchlist', 'price']