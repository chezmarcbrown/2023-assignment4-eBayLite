from django.contrib.auth.models import AbstractUser
from django.db import models

# DONT FORGET TO MIGRATE AFTER CREATING THIS MODEL
# run to migrate changes to database:
#
# > python manage.pymakemigrations
# > python manage.py migrate
#
class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.CharField(max_length=256, blank=True)
    category = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.starting_bid}) "
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.amount} on {self.listing}"
class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.content} on {self.listing}"

class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    username = models.CharField(unique=True, max_length=64)
    bids = models.ManyToManyField(Bid, blank=True, related_name='bids')