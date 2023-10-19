from django.contrib.auth.models import AbstractUser
from django.db import models

category_list = ['Fashion', 'Toys', 'Electronics', 'Home', 'Food']

class User(AbstractUser):
    watchlist = [models.IntegerField(('watch_list'))]
    pass

class Listing(models.Model):
    title = models.CharField(('title'), max_length=150, blank=False)
    category = models.CharField(('category'), max_length=150, blank=False)
    description = models.TextField(('description'), max_length=300, blank=False)
    bid = models.DecimalField(('bid'), decimal_places=2, max_digits=8, blank=False)
    is_active = models.BooleanField(('is active'), default=True, blank=False)
    user = models.ForeignKey(('user'), on_delete=models.PROTECT)
    pass

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass