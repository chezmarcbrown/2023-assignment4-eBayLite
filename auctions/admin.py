from django.contrib import admin

from .models import AuctionListing, Bid, Comment, User

admin.site.register(AuctionListing)

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "amount")
    
admin.site.register(Bid, BidAdmin)


admin.site.register(Comment)


admin.site.register(User)