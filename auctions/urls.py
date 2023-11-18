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
    path("remove_comment/<comment_id>", views.remove_comment, name="remove_comment"),
    path('add_comment/<int:listing_id>/', views.add_comment, name='add_comment'),
    path("remove_bid/<bid_id>", views.remove_bid, name="remove_bid"),
    path("close_listing/<listing_id>", views.close_listing, name="close_listing"),
]
