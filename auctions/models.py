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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions", blank=True, null=True)
    imageURL = models.URLField(blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_seller")
    closed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    update_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated At")

    def __str__(self):
        return f"Auction #{self.id} | Title: {self.title} | Seller: {self.seller} | Closed: {self.closed}"