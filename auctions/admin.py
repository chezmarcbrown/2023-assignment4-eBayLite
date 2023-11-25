from django.contrib import admin
from auctions.models import User, Auction, Category, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
