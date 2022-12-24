from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm

from auctions.models import AuctionItem, AuctionBid


# Create forms


class AuctionForm(ModelForm):
    class Meta:
        model = AuctionItem
        fields = "__all__"
        exclude = ["listed_by"]
        labels = {
            "name": "Item Name",
            "image": "Upload a clear image of your item",
            "image_url": "Image link",
            "category": "Select Item Category",
            "description": "Item Description",
            "price": "Current price",
            "starting_bid": "Bidding price",
        }

    # adding styles to the form by adding the css class to be modified
    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-label'})


class AuctionBidForm(ModelForm):
    class Meta:
        model = AuctionBid
        fields = ["bid"]
        labels = {
            "bid": "Bid Amount:",
        }

    def __init__(self, *args, **kwargs):
        super(AuctionBidForm, self).__init__(*args, **kwargs)

        self.fields['bid'].widget.attrs.update({'class': 'form-control'})