from django.contrib import admin
from .models import Book, Customer, Account, Order


admin.site.register([Book, Customer, Account, Order])
