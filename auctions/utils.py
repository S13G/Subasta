import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

from auctions.models import Watchlist, AuctionItem


def watchlist_items_in_details(request, slug):
    # setting watch-lists in a particular listing
    try:
        item = AuctionItem.objects.get(slug=slug, closed=False)
    except AuctionItem.DoesNotExist:
        raise Http404()

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


def closed_items_in_details(slug):
    try:
        item = AuctionItem.objects.get(slug=slug, closed=True)
    except AuctionItem.DoesNotExist:
        raise Http404()
    other_closed_items = AuctionItem.objects.filter(closed=True)
    if other_closed_items:
        other_closed_items = other_closed_items.exclude(id=item.id)
    # selects and displays 3 random closed items on the detail page
    count = 3
    if other_closed_items.count() < 3:
        count = other_closed_items.count()
    watchlist_items = random.sample(list(other_closed_items), count)
    return item, other_closed_items


def paginate_items(request, items, results):
    page = request.GET.get("page")
    paginator = Paginator(items, results)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        items = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(page)

    # determines how many pagination numbers will be displayed
    left_index = (int(page) - 2)
    right_index = (int(page) + 3)

    if left_index < 1:
        left_index = 1

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, items
