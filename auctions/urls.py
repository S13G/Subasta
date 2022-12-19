from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/", views.all_auctions, name="listings"),
    path("listings/<slug:slug>/", views.category_view, name="category-filter"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register")
]
