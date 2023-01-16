from .models import Book, Customer, Account 
from rest_framework import serializers 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'description', 'count', 'price')
        model = Book


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'surname', 'email', 'city')
        model = Customer
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        print(self.context)
        return super(CustomerSerializer, self).create(validated_data)
