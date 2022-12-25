import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

from auctions.forms import AuctionForm, AuctionBidForm
from auctions.models import AuctionItem, Category, Watchlist, AuctionBid
from auctions.utils import watchlist_items_in_details


def home(request):
    # selects and displays 6 random items on the main page
    featured_items = list(AuctionItem.objects.select_related('category').order_by("-id").all().exclude(closed=True))
    featured_items = random.sample(featured_items, 6)
    context = {"featured_items": featured_items}
    return render(request, "templates/index.html", context)


def all_auctions(request):
    categories = Category.objects.all()
    items = AuctionItem.objects.all().exclude(closed=True)
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
    item, watchlist_items = watchlist_items_in_details(request, slug)
    if request.user != item.listed_by and request.method == "POST":
        form = AuctionBidForm(request.POST)
        if form.is_valid():
            bid_price = form.save(commit=False)
            bid_price.bidder = request.user
            bid_price.item = item

            # checking if the bid price is less than the starting bid specified by the item owner
            if bid_price.bid <= item.starting_bid:
                messages.info(request, "Your bid is less than the starting price or less than the other bidder's bid")
            else:
                # checking if the last bid before the new bid exists and if it's greater than the new bid made
                if item.bids.exists() and item.bids.last().bid >= bid_price.bid:
                    messages.info(request, "Bid a price larger than the previous bidder")
                else:
                    bid_price.save()
                    messages.success(request,
                                     "You've successfully placed a bid of ${} on {}".format(bid_price.bid,
                                                                                            bid_price.item.name))

            return HttpResponseRedirect(f'/listings/item/{slug}/')
        messages.error(request, "Bid wasn't successful, Try again")
    else:
        form = AuctionBidForm()

    # if number of bids appearing in the template is more than 3, get the 3 latest bids
    previous_bids = AuctionBid.objects.filter(item=item).order_by("-created")
    if previous_bids.count() > 3:
        previous_bids = previous_bids[:3]

    context = {"item": item, "watchlist_items": watchlist_items, "form": form, "previous_bids": previous_bids}
    return render(request, "auctions/auction-detail.html", context)


@login_required(login_url="login")
def watchlist_item(request):
    owner = request.user
    watchlist_items = Watchlist.objects.filter(user=owner)
    context = {"watchlist_items": watchlist_items, "owner": owner}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url="login")
def add_to_watchlist(request, item_id):
    item = get_object_or_404(AuctionItem, id=item_id, closed=False)
    Watchlist.objects.get_or_create(user=request.user, item=item)
    return HttpResponseRedirect(reverse('watchlist-items'))


@login_required(login_url="login")
def remove_from_watchlist(request, item_id):
    item = get_object_or_404(Watchlist, id=item_id)
    # if item belongs to the current authenticated user, remcve it
    if item.user == request.user:
        item.delete()
    return HttpResponseRedirect(reverse('watchlist-items'))


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


def close_auction(request, slug):
    item = get_object_or_404(AuctionItem, slug=slug, closed=False)
    if item.listed_by == request.user:
        item.closed = True
        item.save()
        messages.info(request, "You closed an auction on {}".format(item.name))
    return HttpResponseRedirect(reverse("listings"))