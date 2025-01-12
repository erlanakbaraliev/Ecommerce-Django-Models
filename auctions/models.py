from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"@{self.user}: {self.bid}$"
    
class Listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=400)
    image_url = models.URLField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing")
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")
    bidCount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    leadingUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leadingUser", null=True)

    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=400)

    def __str__(self):
        return f"@{self.author}: {self.message}"
    