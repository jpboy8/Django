from django.contrib import admin
from .models import Customer, Account, Deposit

admin.site.register([Customer, Account, Deposit])
