from .models import Book, Customer, Account, Deposit, Order
from rest_framework import serializers
import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'price')
        model = Book


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'author', 'price', 'description', 'count')
        model = Book


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'surname', 'email', 'city')
        model = Customer
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'balance')
        model = Account
        read_only_fields = ['id', 'balance']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(AccountSerializer, self).create(validated_data)


class DepositSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(DepositSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            # if u want to add this with pretty rest framework interface, then write  "self.fields['account'].queryset" instead of "self.fields['account']"
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user.id)

    def create(self, validated_data):
        try:
            validated_data['amount']
        except Exception as ex:
            print(ex)
            raise serializers.ValidationError(
                'You have to fill amount field'
            )
        if validated_data['amount'] <= 0:
            raise serializers.ValidationError(
                ('amount must be greater than zero')
            )
        else:

            if validated_data['account'].balance + validated_data['amount'] > 0:
                validated_data['account'].balance += validated_data['amount']
                validated_data['account'].save()
            else:
                raise serializers.ValidationError(
                    ('Not enough money')
                )
            return super(DepositSerializer, self).create(validated_data)

    class Meta:
        fields = ('id', 'date', 'amount', 'account')
        model = Deposit
        read_only_fields = ['id', 'date']


class OrderSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['customer'].queryset = self.fields['customer']\
                .queryset.filter(user=self.context['view'].request.user.id)

    def validate(self, data):
        try:
            data['book'] = Book.objects.get(pk=data['book'].id)
            data['date'] = datetime.datetime.now().date()
        except Exception:
            raise serializers.ValidationError(
                ('No such book')
            )
        return data

    class Meta:
        fields = ('id', 'customer', 'book', 'date')
        model = Order
        read_only_fields = ['id', 'date']
