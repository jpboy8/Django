from django.contrib.auth.models import User
from .models import Book, Customer, Account, Deposit, Order, Cart, Cartitems, CartOrder
from rest_framework import serializers
import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'price')
        model = Book


class SimleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']
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

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'customer', 'book', 'date')
        model = Order
        read_only_fields = ['id', 'date']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class CartItemSerializer(serializers.ModelSerializer):
    book = SimleBookSerializer()
    sub_total = serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = Cartitems
        fields = ['id', 'cart', 'book', 'quantity', 'sub_total']

    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.book.price

class CartSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            # if u want to add this with pretty rest framework interface, then write  "self.fields['account'].queryset" instead of "self.fields['account']"
            self.fields['owner'].queryset = self.fields['owner']\
                .queryset.filter(user=self.context['view'].request.user.id)
            
    id = serializers.UUIDField(read_only=True)
    price = serializers.SerializerMethodField(method_name='main_total')
    count = serializers.SerializerMethodField(method_name='items_count')

    class Meta:
        model = Cart    
        fields = ["id", 'owner', 'count',"price"]
    
    def items_count(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity for item in items])

        return total
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.book.price for item in items])
        return total



class AddCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is not book associated with the given ID")
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        book_id = self.validated_data["book_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = Cartitems.objects.get(book_id=book_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = Cartitems
        fields = ['id', 'book_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields = ["quantity"]


class CartOrderSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            acc = Account.objects.get(user=self.context['view'].request.user.id)
            self.fields['customer'].queryset = self.fields['customer']\
                .queryset.filter(user=self.context['view'].request.user.id)
            self.fields['cart'].queryset = self.fields['cart']\
                .queryset.filter(owner=acc.id)
    
    def validate(self, data):
        try:
            data['cart'] = Cart.objects.get(pk=data['cart'].id)
            data['date'] = datetime.datetime.now().date()
        except Exception:
            raise serializers.ValidationError(
                ('No such book')
            )
        return data

    class Meta:
        model = CartOrder
        fields = ('id', 'customer', 'cart', 'date')
        read_only_fields = ['id', 'date']