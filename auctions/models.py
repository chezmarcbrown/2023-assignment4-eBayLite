from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', related_name='watchlist', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

class Auction(models.Model):

    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='auction_listing')
    image_url = models.URLField(default='', blank=True, null=True)
    closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=96, blank=True, null=True)
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    bid = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self) -> str:
        return f"{self.user.username} bid {self.bid} on {self.auction.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.username} commented: {self.comment} on {self.auction.title}"