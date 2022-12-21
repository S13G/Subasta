import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse

from auctions.forms import AuctionForm
from auctions.models import AuctionItem, Category


def home(request):
    # selects and displays 6 random items on the main page
    featured_items = list(AuctionItem.objects.select_related('category').order_by("-id").all())
    featured_items = random.sample(featured_items, 6)
    return render(request, "templates/index.html")


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


@login_required(login_url="login")
def item_details(request, slug):
    item = AuctionItem.objects.get(slug=slug)
    # selects and displays 3 random watchlist items on the detail page
    watchlist_items = list(AuctionItem.objects.filter(watchlist=True).exclude(id=item.id))
    watchlist_items = random.sample(watchlist_items, 3)
    context = {"item": item, "watchlist_items": watchlist_items}
    return render(request, "auctions/auction-detail.html", context)


@login_required(login_url="login")
def watchlist_item(request):
    owner = request.user
    items = owner.item.filter(watchlist=True)
    context = {"items": items, "owner": owner}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url="login")
def create_listing(request):
    owner = request.user

    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction_item = form.save(commit=False)
            auction_item.listed_by = owner
            auction_item.save()

            messages.success(request, "Item {} has been added successfully".format(auction_item.name))

            return HttpResponseRedirect(reverse('listings'))
        messages.error(request, "Error adding item")
        return render(request, "auctions/create-listing.html", {"form": form})
    else:
        form = AuctionForm()
        return render(request, "auctions/create-listing.html", {"form": form})
