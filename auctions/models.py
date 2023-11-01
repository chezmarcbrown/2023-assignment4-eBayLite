from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length = 60)

    def __str__(self):
        return f"{self.title}"
    
class Auction(models.Model):
    title = models.CharField(max_length = 60)
    description = models.TextField(max_length = 480)
    starting_price = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    current_bid = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions", blank=True, null=True)
    imageURL = models.URLField(blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_seller")
    closed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    update_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated At")

    def __str__(self):
        return f"Auction #{self.id} /n Title: {self.title} /n Seller: {self.seller} /n Closed: {self.closed}"
    

class Watchlist(models.Model):
    auctions = models.ManyToManyField(Auction, related_name="watchlists")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user}'s watchlist"
    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bidder.username} bid ${self.bid_price} on {self.auction.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    headline = models.CharField(max_length=64)
    message = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.username} comments on {self.auction.title}"    