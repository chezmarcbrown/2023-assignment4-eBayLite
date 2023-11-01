from django.urls import path

from . import views
app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("create/", views.create, name="create"),
    path("<int:auction_id>/", views.auction, name="auctions"),
    path("categories/", views.categories, name="categories"),
    path("<str:category>", views.filterCategories, name="category"),

    path("watchlist/", views.watchlist, name="watchlist"),
    path("watch/<int:auction_id>", views.watch, name="watch"),
    path("unwatch/<int:auction_id>", views.unwatch, name="unwatch"),

    path("comment/<int:auction_id>", views.comment, name="comment"),

    path("updatebid/<int:bid_id>/<int:auction_id>", views.updatebid, name="updatebid"),
    path("closebid/<int:auction_id>", views.closebid, name="closebid")
]
