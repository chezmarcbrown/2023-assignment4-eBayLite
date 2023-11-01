from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listings/<int:auction_id>", views.listings, name="listing"),
    path("listings/<int:auction_id>/bid", views.bidding, name="bid"),
    path("listings/<int:auction_id>/close", views.close, name="close"),
    path("listings/<int:auction_id>/comment", views.comment, name="comment"),
    path("listings/<int:auction_id>/add", views.add, name="add"),
    path("listings/<int:auction_id>/remove", views.remove, name="remove")
]
