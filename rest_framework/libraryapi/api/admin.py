from django.contrib import admin
from .models import Book, Customer, Account
# Register your models here.

admin.site.register([Book, Customer, Account])