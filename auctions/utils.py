import random

from auctions.models import Watchlist, AuctionItem


def watchlist_items_in_details(request, slug):
    # setting watch-lists in a particular listing
    item = AuctionItem.objects.get(slug=slug, closed=False)
    try:
        watchlist_item = Watchlist.objects.get(user=request.user, item=item)
    except Watchlist.DoesNotExist:
        watchlist_item = None
    if watchlist_item:
        watchlist_items = Watchlist.objects.filter(user=request.user).exclude(id=watchlist_item.id)
    else:
        watchlist_items = Watchlist.objects.filter(user=request.user)
    # selects and displays 3 random watchlist items on the detail page
    count = 3
    if watchlist_items.count() < 3:
        count = watchlist_items.count()
    watchlist_items = random.sample(list(watchlist_items), count)
    return item, watchlist_items
