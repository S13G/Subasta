import random

# from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from auctions.models import AuctionItem, Category


def home(request):
    featured_items = AuctionItem.objects.select_related('category').order_by("-id").all()[:6:-1]
    context = {"featured_items": featured_items}
    return render(request, "templates/index.html", context)


def all_auctions(request):
    categories = Category.objects.all()
    items = AuctionItem.objects.all()
    context = {"categories": categories, "items": items}
    return render(request, "auctions/all-auctions.html", context)


def category_view(request, slug):
    categories = Category.objects.all()
    try:
        category = categories.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404()
    items = category.items.all()
    context = {"items": items, "category": category, "categories": categories}
    return render(request, "auctions/auction-filter.html", context)


# @login_required('login')
def item_details(request, slug):
    item = AuctionItem.objects.get(slug=slug)
    watchlist_items = AuctionItem.objects.filter(watchlist=True).exclude(id=item.id).distinct()[:3:-1]
    random.shuffle(watchlist_items)
    context = {"item": item, "watchlist_items": watchlist_items}
    return render(request, "auctions/auction-detail.html", context)


# @login_required('login')
def watchlist_item(request):
    items = AuctionItem.objects.filter(watchlist=True)
    context = {"items": items}
    return render(request, "auctions/watchlist.html", context)
