from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("showCategory/", views.showCategory, name = "showCategory"),
    path("listings/<int:id>", views.listings, name="listings"),
    path('watchlist/', views.displayWatchList, name='watchlist'),
    path('removeWatchList/<int:id>/', views.removeWatchList, name='removeWatchList'),
    path('addWatchList/<int:id>/', views.addWatchList, name='addWatchList'),
    path('addComment/<int:id>/', views.addComment, name='addComment'),
    path('addBid/<int:id>/', views.addBid, name='addBid'),
    path('closeAuction/<int:id>/', views.closeAuction, name='closeAuction'),
    path('categories', views.categories, name='categories'),
    path('categoryList/<int:id>/', views.categoryList, name='categoryList')
]
