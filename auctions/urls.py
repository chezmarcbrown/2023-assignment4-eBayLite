from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path('<int:auction_id>/', views.auction, name="auction"),
    path("categories/", views.categories, name="categories"),
    path("<str:cat_name>", views.category, name="category"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("addwishlist/<int:auction_id>", views.addwishlist, name="addwishlist"),
    path("removewishlist/<int:auction_id>", views.removewishlist, name="removewishlist"),
    path("makebid/<int:bid_id>/<int:auction_id>", views.makebid, name="makebid"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("closebid/<int:auction_id>", views.closebid, name="closebid"),
    path('toggle_watchlist/<int:listing_id>/', views.toggle_watchlist, name='toggle_watchlist'),
   # path("api/status", views.api_status, name="api_status"),

]
