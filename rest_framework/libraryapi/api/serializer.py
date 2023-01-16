from .models import Book, Customer, Account 
from rest_framework import serializers 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'description', 'count', 'price')
        model = Book