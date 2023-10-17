from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing():
    title = models.CharField(('title'), max_length=150, blank=False)
    description = models.TextField(('description'), max_length=300, blank=False)
    bid = models.DecimalField(('bid'), decimal_places=2, blank=False)
    is_active = models.BooleanField(('is active'), default=True, blank=False)
    pass

class Bid():
    pass

class Comment():
    pass