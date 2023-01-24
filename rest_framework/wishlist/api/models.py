from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Wishlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Item(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.name
