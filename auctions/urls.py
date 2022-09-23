from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listings, name="create"),
    path("listing-detail/<str:pk>/", views.listing_details, name="details"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("delete-watchlist/<str:pk>/ ", views.delete_watchlist, name="delete_watchlist"),
]
