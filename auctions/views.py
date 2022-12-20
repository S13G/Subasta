import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from auctions.models import User, AuctionItem, Category


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
    watchlist_items = AuctionItem.objects.filter(watchlist=True).distinct()[:3:-1]
    # TODO
    # turn the watchlist_items into a values list(flat=true) iterate over the list checking
    # if the item is already in the list, if it is then remove the item from the list,
    # this could be a property or a logic in the view
    random.shuffle(watchlist_items)
    context = {"item": item, "watchlist_items": watchlist_items}
    return render(request, "auctions/auction-detail.html", context)


# @login_required('login')
def watchlist_item(request):
    items = AuctionItem.objects.filter(watchlist=True)
    context = {"items": items}
    return render(request, "auctions/watchlist.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Error logging in")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Successfully logged out")
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords don't match")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.info(request, "Username has already been taken")
            return render(request, "auctions/register.html")
        login(request, user)
        messages.success(request, "Logged in successfully")
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "auctions/register.html")
