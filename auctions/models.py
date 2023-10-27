from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wishlist = models.ManyToManyField('Auction', related_name='wishlist', blank=True)

class Auction(models.Model):

    FASHION = "Fashion"
    TOYS = "Toys"
    ELECTRONICS = "Electronics"
    HOME = "Home"

    CATEGORIES = [
        (FASHION, "Fashion"),
        (TOYS, "Toys"),
        (ELECTRONICS, "Electronics"),
        (HOME, "Home")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    #starting_bid = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, blank=False)
    image_url = models.URLField(default='')
    #bid_counter = models.IntegerField(default=1)
    #created_at = models.DateTimeField(auto_now_add=True)
    #active = models.BooleanField(default=True)
    #winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.title}: made by {self.user.username}'
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)# the user making the bid
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)# the auction they are bidding on
    bid =  models.DecimalField(decimal_places=2, max_digits=8)# the amount they are bidding for

    def __str__(self):
        return f'{self.user.username} bidded {self.bid} on {self.auction.title}'# /admin displays this
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username} commented: {self.comment} on {self.auction.title}'