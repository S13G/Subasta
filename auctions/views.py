from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from auctions.forms import CreateForm, PlaceBidForm

from .models import AuctionBid, User, AuctionItem


def index(request):
    auctions = AuctionItem.objects.all()
    context = {"auctions": auctions}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_listings(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
        return redirect('create')
    else:
        form = CreateForm(user=request.user)
    context = {"form": form, "message": "Please fill form properly"}
    return render(request, "auctions/create.html", context)


def listing_details(request, pk):
    auction_item = get_object_or_404(AuctionItem, id=pk)
    bids = auction_item.bids.all()
    if request.method == "POST":
        bid_form = PlaceBidForm(data=request.POST, user=request.user)
        if bid_form.is_valid():
            bid_form.cleaned_data["bid"]
            bid_form.instance.user = request.user
            new_bid = bid_form.save(commit=False)
            new_bid.auction_item = auction_item
            new_bid.save()
            messages.success(request, "Bid has been successfully made")
        else:
            messages.error(request, "Bid wasn't made successfully")
    else:
        bid_form = PlaceBidForm()
    context = {'auction_item': auction_item, "bid_form": bid_form, "bids": bids}
    return render(request, 'auctions/details.html', context)


@login_required(login_url='login')
def watchlist(request):
    verified_auction = AuctionItem.objects.filter(watchlist=True)
    verified_auction_count = verified_auction.count()
    context = {"verified_auction": verified_auction, "count": verified_auction_count}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='login')
def delete_watchlist(request, pk):
    verified_auction = AuctionItem.objects.get(id=pk)
    if request.method == "POST":
        verified_auction.delete()
        return redirect('watchlist')
    context = {"verified_auction": verified_auction, "message": "Watchlist item deleted"}
    return render(request, "auctions/delete_watchlist.html", context)