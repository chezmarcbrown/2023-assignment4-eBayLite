from django.contrib import admin
from auctions.models import Auction, Category

# Register your models here.
admin.site.register(Auction)
admin.site.register(Category)