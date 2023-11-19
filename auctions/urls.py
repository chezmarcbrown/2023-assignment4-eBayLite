from django.urls import path
from django.urls import reverse

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

from . import views

app_name = "auctions"
urlpatterns = [
    path('', views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new/", views.create_listing, name="create_listing"),
    path("categories/", views.category, name="categories"),
    path("category/<int:category_id>/", views.category_listings, name="category_listings"),
    path("watchlist/", views.watchlist_view, name="watchlist_view"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('watchlist/<int:auction_id>/', views.watchlist, name='watchlist'),
    path('remove_from_watchlist/<int:auction_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('get-comments/<int:listing_id>/', views.getComments, name='get_comments'),
    path('comment/<int:listing_id>/', views.comment, name='comment'),
    path("close_listing/<int:listing_id>/", views.close_listing, name="close_listing"),

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
