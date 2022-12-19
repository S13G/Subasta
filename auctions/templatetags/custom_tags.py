from django import template

from auctions.models import AuctionItem

register = template.Library()


@register.simple_tag
def watchlist_count():
    watchlist_item_count = AuctionItem.objects.filter(watchlist=True).count()
    return watchlist_item_count
