import random

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect

from auctions.forms import AuctionBidForm, CommentForm
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


def auction_bid_form_in_item(request, slug):
    try:
        item = AuctionItem.objects.get(slug=slug, closed=False)
    except AuctionItem.DoesNotExist:
        raise Http404()
    if request.user != item.listed_by and request.method == "POST":
        auction_bid_form = AuctionBidForm(request.POST)
        if auction_bid_form.is_valid():
            bid_price = auction_bid_form.save(commit=False)
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
        auction_bid_form = AuctionBidForm()
    return auction_bid_form


def comment_form_in_item(request, slug):
    try:
        item = AuctionItem.objects.get(slug=slug, closed=False)
    except AuctionItem.DoesNotExist:
        raise Http404()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.item = item
            comment.owner = request.user
            comment.save()
            messages.success(request, "Comment added to {} successfully".format(item))
        else:
            messages.info(request, "Error processing request")
    else:
        comment_form = CommentForm()
    return comment_form
