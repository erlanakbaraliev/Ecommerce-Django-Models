from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    amount = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Amount: {self.amount}"
    
    
class Category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName

class Auction(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=400)
    image_url = models.URLField(max_length=1000)
    price = models.FloatField()
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return self.title