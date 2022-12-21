from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/", views.all_auctions, name="listings"),
    path("listings/<slug:slug>/", views.category_view, name="category-filter"),
    path("listings/item/<slug:slug>", views.item_details, name="item-details"),
    path("watchlist/", views.watchlist_item, name="watchlist-items"),
    path("create-listing/", views.create_listing, name="create-listings")
]
