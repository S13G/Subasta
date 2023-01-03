import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404, redirect

from auctions.forms import AuctionForm, CommentForm, AuctionBidForm
from auctions.models import AuctionItem, Category, Watchlist, AuctionBid
from auctions.utils import watchlist_items_in_details, closed_items_in_details


def home(request):
    # this function selects and displays 6 random items on the main page
    featured_items = AuctionItem.objects.select_related('category').order_by("-id").all().exclude(closed=True)
    count = 6
    if featured_items.count() < 6:
        count = featured_items.count()
    featured_items = random.sample(list(featured_items), count)
    context = {"featured_items": featured_items}
    return render(request, "templates/index.html", context)


def all_auctions(request):
    # this function handles all categories and active listings
    categories = Category.objects.all()
    items = AuctionItem.objects.all().exclude(closed=True)
    context = {"categories": categories, "items": items}
    return render(request, "auctions/all-auctions.html", context)


def category_view(request, slug):
    # this function returns item filtered by their category
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
    # handles the item details, auction and comment form including the logic
    item, watchlist_items = watchlist_items_in_details(request, slug)
    auction_bid_form = AuctionBidForm()
    all_comments = item.comments.all()
    comment_form = CommentForm()

    # if number of bids appearing in the template is more than 3, get the 3 latest bids
    previous_bids = AuctionBid.objects.filter(item=item).order_by("-created")
    if previous_bids.count() > 3:
        previous_bids = previous_bids[:3]

    context = {"item": item, "watchlist_items": watchlist_items, "auction_bid_form": auction_bid_form,
               "previous_bids": previous_bids, "comment_form": comment_form, "all_comments": all_comments}
    return render(request, "auctions/auction-detail.html", context)


@login_required(login_url="login")
def watchlist_item(request):
    # displays the watchlist items of each user and filter by search
    owner = request.user
    watchlist_items = Watchlist.objects.filter(user=owner)
    results = []
    if request.method == "GET":
        watchlist_search_query = request.GET.get("watchlist-search-query")
        if watchlist_search_query is not None:
            results = watchlist_items.filter(
                Q(item__name__icontains=watchlist_search_query) | Q(item__price__icontains=watchlist_search_query) |
                Q(item__listed_by__first_name__icontains=watchlist_search_query) |
                Q(item__listed_by__last_name__icontains=watchlist_search_query) |
                Q(item__description__icontains=watchlist_search_query))
    context = {"watchlist_items": watchlist_items, "owner": owner, "results": results,
               "watchlist_search_query": watchlist_search_query}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url="login")
def add_to_watchlist(request, item_id):
    # adds a particular item to a user's watchlist
    item = get_object_or_404(AuctionItem, id=item_id, closed=False)
    Watchlist.objects.get_or_create(user=request.user, item=item)
    messages.info(request, "{} has been added to watchlist".format(item.name))
    return HttpResponseRedirect(reverse('watchlist-items'))


@login_required(login_url="login")
def remove_from_watchlist(request, item_id):
    # removes a particular item to a user's watchlist
    item = get_object_or_404(Watchlist, id=item_id)
    # if item belongs to the current authenticated user, remove it
    if item.user == request.user:
        item.delete()
        messages.info(request, "{} has been removed from watchlist".format(item.item.name))
    return HttpResponseRedirect(reverse('watchlist-items'))


@login_required(login_url="login")
def create_listing(request):
    # handles the creation of a new auction item by the user
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
    # handles the closing of an auction
    item = get_object_or_404(AuctionItem, slug=slug, closed=False)
    # if bids exists for the item and the logged in user is the lister, auction can be closed
    if item.bids.exists() and item.listed_by == request.user:
        winner = item.bids.last().bidder
        last_bidder = f"{winner.first_name} {winner.last_name}"
        item.closed = True
        item.winner = winner
        messages.success(request, "You closed an auction on {} and {} won the auction".format(item.name, last_bidder))
        item.save()
    else:
        item.closed = True
        messages.success(request, "You closed an auction on {}".format(item.name))
        item.save()
    return HttpResponseRedirect(reverse("listings"))


@login_required(login_url="login")
def closed_listings(request):
    # displays all closed items
    categories = Category.objects.all()
    closed_items = AuctionItem.objects.filter(closed=True)
    results = []
    if request.method == "GET":
        closed_search_query = request.GET.get("closed-search-query")
        if closed_search_query is not None:
            results = AuctionItem.objects.filter(
                Q(name__icontains=closed_search_query) | Q(price__icontains=closed_search_query) |
                Q(listed_by__first_name__icontains=closed_search_query) |
                Q(listed_by__last_name__icontains=closed_search_query) |
                Q(description__icontains=closed_search_query), closed=True)
    context = {"closed_items": closed_items, "categories": categories, "closed_search_query": closed_search_query,
               "results": results}
    return render(request, "auctions/closed-listings.html", context)


@login_required(login_url="login")
def closed_category_view(request, slug):
    # displays the closed items filtered by their category
    categories = Category.objects.all()
    try:
        category = categories.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404()
    closed_items = category.items.filter(closed=True)
    context = {"closed_items": closed_items, "category": category, "categories": categories}
    return render(request, "auctions/closed-auction-filter.html", context)


@login_required(login_url="login")
def closed_item_details(request, slug):
    # handles closed item details and comments
    item, other_closed_item = closed_items_in_details(slug)
    all_comments = item.comments.all()
    # if bids exist, the last bidder is the winner
    try:
        item_winner = item.bids.last().bidder
    except:
        item_winner = None
    item_bidders = item.auction_item_bidders
    # if number of bids appearing in the template is more than 3, get the 3 latest bids
    previous_bids = AuctionBid.objects.filter(item=item).order_by("-created")
    if previous_bids.count() > 3:
        previous_bids = previous_bids[:3]
    context = {"item": item, "other_closed_items": other_closed_item, "item_winner": item_winner,
               "previous_bids": previous_bids, "item_bidders": item_bidders, "all_comments": all_comments}
    return render(request, "auctions/closed-auction-detail.html", context)


# this function handles the auction form view
# passes the url of the view in the action of the form template
@login_required(login_url="login")
def auction_bid_form_in_item(request, item_slug):
    # handles the place bid form in the item
    try:
        item = AuctionItem.objects.get(slug=item_slug, closed=False)
    except AuctionItem.DoesNotExist:
        raise Http404()
    if request.user != item.listed_by and request.method == "POST" and "auction-btn" in request.POST:
        auction_bid_form = AuctionBidForm(request.POST)
        if auction_bid_form.is_valid():
            bid_price = auction_bid_form.save(commit=False)
            bid_price.bidder = request.user
            bid_price.item = item

            # checking if the bid price is less than the starting bid specified by the item owner
            if bid_price.bid <= item.starting_bid:
                messages.error(request, "Your bid is less than the starting price")
            else:
                # checking if the last bid before the new bid exists and if it's greater than the new bid made
                if item.bids.exists() and item.bids.last().bid >= bid_price.bid:
                    messages.error(request, "Bid a price larger than the previous bidder")
                else:
                    bid_price.save()

                    messages.success(request,
                                     "You've successfully placed a bid of ${} on {}".format(bid_price.bid,
                                                                                            bid_price.item.name))

            return redirect(f'/listings/item/{item.slug}/')
        messages.error(request, "Bid wasn't successful, Try again")


@login_required(login_url="login")
def comment_form_in_item(request, item_slug):
    # this function handles the comment form view
    # passes the url of the view in the action of the form template
    try:
        item = AuctionItem.objects.get(slug=item_slug, closed=False)
    except AuctionItem.DoesNotExist:
        raise Http404()
    if request.method == "POST" and "comment-btn" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.item = item
            comment.owner = request.user
            comment.save()
            messages.success(request, "Comment added to {} successfully".format(item))
        else:
            messages.info(request, "Error processing request")
        return redirect(f'/listings/item/{item.slug}/')


# search function for the all listings page
def search(request):
    categories = Category.objects.all()
    results = []
    search_query = None
    if request.method == "GET":
        search_query = request.GET.get("search-query")
        if search_query is not None:
            results = AuctionItem.objects.filter(Q(name__icontains=search_query) | Q(price__icontains=search_query) |
                                                 Q(listed_by__first_name__icontains=search_query) |
                                                 Q(listed_by__last_name__icontains=search_query) |
                                                 Q(description__icontains=search_query), closed=False)
        else:
            search_query = 'None'
            messages.info(request, "Empty search query")
    context = {"search_query": search_query, "results": results, "categories": categories}
    return render(request, "auctions/search-items.html", context)


@login_required(login_url='login')
def dashboard(request):
    total_items_won = request.user.items_won.all().count()
    total_items_listed = request.user.item.count()
    total_items_closed = AuctionItem.objects.filter(closed=True, listed_by=request.user).count()
    total_watchlist_items = request.user.watchlists.count()
    context = {"total_items_won": total_items_won, "total_items_listed": total_items_listed,
               "total_items_closed": total_items_closed, "total_watchlist_items": total_watchlist_items}
    return render(request, "auctions/dashboard.html", context)
