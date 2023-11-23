from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length = 60)

    def __str__(self):
        return self.title
    
class Auction(models.Model):
    title = models.CharField(max_length = 60)
    description = models.CharField(max_length = 480)
    price = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    imageUrl = models.CharField(max_length = 1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_seller")
    closed = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="WatchList")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    update_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated At")

    def __str__(self):
        return self.title
class Bid(models.Model):
    bid = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBid")

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auctionComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.author}"    
    