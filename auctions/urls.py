from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<listing_id>", views.listing, name="listing"),
    path("categories/", views.categories, name="categories"),
    path("watchlist_add_or_remove/<listing_id>", views.watchlist_add_or_remove, name="watchlist_add_or_remove"),
    path("remove_listing/<listing_id>", views.remove_listing, name="remove_listing"),
]
