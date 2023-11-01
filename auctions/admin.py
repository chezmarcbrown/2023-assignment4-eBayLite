from django.contrib import admin
from auctions.models import Auction, Category, Watchlist, Bid, Comment

# Register your models here.
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment)