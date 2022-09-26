from django import forms

from auctions.models import AuctionBid, AuctionItem


class CreateForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['item_name', 'image', 'image_url', 'category', 'description', 'price', 'starting_bid']


class PlaceBidForm(forms.ModelForm):    
    class Meta:
        model = AuctionBid
        fields = ['bid']