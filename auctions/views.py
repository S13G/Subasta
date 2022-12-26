import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

from auctions.forms import AuctionForm
from auctions.models import AuctionItem, Category, Watchlist, AuctionBid
from auctions.utils import watchlist_items_in_details, closed_items_in_details, auction_bid_form_in_item, \
    comment_form_in_item


def home(request):
    # selects and displays 6 random items on the main page
    featured_items = AuctionItem.objects.select_related('category').order_by("-id").all().exclude(closed=True)
    count = 6
    if featured_items.count() < 6:
        count = featured_items.count()
    featured_items = random.sample(list(featured_items), count)
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
    auction_bid_form = auction_bid_form_in_item(request, slug)
    comment_form, all_comments = comment_form_in_item(request, slug)
    # if number of bids appearing in the template is more than 3, get the 3 latest bids
    previous_bids = AuctionBid.objects.filter(item=item).order_by("-created")
    if previous_bids.count() > 3:
        previous_bids = previous_bids[:3]

    context = {"item": item, "watchlist_items": watchlist_items, "auction_bid_form": auction_bid_form,
               "previous_bids": previous_bids, "comment_form": comment_form, "all_comments": all_comments}
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
    messages.info(request, "{} has been added to watchlist".format(item.name))
    return HttpResponseRedirect(reverse('watchlist-items'))


@login_required(login_url="login")
def remove_from_watchlist(request, item_id):
    item = get_object_or_404(Watchlist, id=item_id)
    # if item belongs to the current authenticated user, remove it
    if item.user == request.user:
        item.delete()
        messages.info(request, "{} has been removed from watchlist".format(item.item.name))
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


@login_required(login_url="login")
def close_auction(request, slug):
    item = get_object_or_404(AuctionItem, slug=slug, closed=False)
    if item.bids.exists() and item.listed_by == request.user:
        last_bidder = f"{item.bids.last().bidder.first_name} {item.bids.last().bidder.last_name}"
        item.closed = True
        messages.success(request, "You closed an auction on {} and {} won the auction".format(item.name, last_bidder))
        item.save()
    else:
        item.closed = True
        messages.success(request, "You closed an auction on {}".format(item.name))
        item.save()
    return HttpResponseRedirect(reverse("listings"))


@login_required(login_url="login")
def closed_listings(request):
    categories = Category.objects.all()
    closed_items = AuctionItem.objects.filter(closed=True)
    context = {"closed_items": closed_items, "categories": categories}
    return render(request, "auctions/closed-listings.html", context)


@login_required(login_url="login")
def closed_category_view(request, slug):
    categories = Category.objects.all()
    try:
        category = categories.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404()
    closed_items = category.items.filter(closed=True)
    context = {"closed_items": closed_items, "category": category, "categories": categories}
    return render(request, "auctions/closed-auction-filter.html", context)


@login_required(login_url="login")
def closed_item_details(request, slug, comments):
    item, other_closed_item = closed_items_in_details(slug)
    all_comments = comment_form_in_item(request, slug, comments)
    try:
        item_winner = item.bids.last().bidder
    except AuctionItem.DoesNotExist:
        item_winner = None
    item_bidders = item.auction_item_bidders
    # if number of bids appearing in the template is more than 3, get the 3 latest bids
    previous_bids = AuctionBid.objects.filter(item=item).order_by("-created")
    if previous_bids.count() > 3:
        previous_bids = previous_bids[:3]
    context = {"item": item, "other_closed_items": other_closed_item, "item_winner": item_winner,
               "previous_bids": previous_bids, "item_bidders": item_bidders, "all_comments": all_comments}
    return render(request, "auctions/closed-auction-detail.html", context)
