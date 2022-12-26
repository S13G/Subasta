from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/", views.all_auctions, name="listings"),
    path("listings/<slug:slug>/", views.category_view, name="category-filter"),
    path("add_to_watchlist/<str:item_id>/", views.add_to_watchlist, name="add-to-watchlist"),
    path("remove_from_watchlist/<str:item_id>/", views.remove_from_watchlist, name="remove-from-watchlist"),
    path("listings/item/<slug:slug>/", views.item_details, name="item-details"),
    path("watchlist/", views.watchlist_item, name="watchlist-items"),
    path("create_listing/", views.create_listing, name="create-listings"),
    path("close_auction/<slug:slug>", views.close_auction, name="close-auction"),
    path("closed_listings/", views.closed_listings, name="closed-listings"),
    path("closed_listings/<slug:slug>/", views.closed_category_view, name="closed-category-filter"),
    path("closed_listings/item/<slug:slug>/", views.closed_item_details, name="closed-item-details"),
    path("comment/<slug:item_slug>/", views.comment_form_in_item, name="comment"),
    path("auction/<slug:item_slug>/", views.auction_bid_form_in_item, name="auction_bid")
]
