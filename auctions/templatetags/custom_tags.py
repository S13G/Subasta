from django import template

from auctions.models import Watchlist, AuctionItem

register = template.Library()


@register.simple_tag
def watchlist_count(request):
    # access user by passing request as a parameter and as argument in the template
    owner = request.user
    watchlist_item_count = Watchlist.objects.filter(user=owner).count()
    return watchlist_item_count


@register.filter
def check_watchlist_item_existence(item, request):
    item = Watchlist.objects.filter(item=item, user=request.user)
    if item.exists():
        return True
    return False


@register.simple_tag
def closed_listing_count():
    # access user by passing request as a parameter and as argument in the template
    closed_items_count = AuctionItem.objects.filter(closed=True).count()
    return closed_items_count
