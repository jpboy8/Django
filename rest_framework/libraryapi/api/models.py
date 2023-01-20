from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=70)
    description = models.TextField()
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    city = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Account(models.Model):
    balance = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    date = models.DateField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.name
