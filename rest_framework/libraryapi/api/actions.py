from .models import Account, Book, Cart, Cartitems
from django.db import transaction
from django.core.exceptions import ValidationError


def make_order(account, book):

    if book.count == 0:
        raise ValidationError('Book is empty')

    if account.balance < book.price:
        raise ValidationError("You don't have enough money")

    with transaction.atomic():
        account_balance = account.balance - book.price
        account.balance = account_balance
        account.save()

        book_count = book.count - 1
        book.count = book_count
        book.save()

def make_order_cart(account, cart):
    items = Cartitems.objects.filter(cart=cart)
    price = sum([item.quantity * item.book.price for item in items])

    if account.balance < price:
        raise ValidationError("You don't have enough money")
    
    for item in items:
        if item.book.count < item.quantity:
            raise ValidationError(f"There are not enough copies of this book in stock: {item.book.title}")

    with transaction.atomic():
        for item in items:
            item.book.count -= item.quantity
            item.book.save()
            item.delete()

        account_balance = account.balance - price
        account.balance = account_balance
        account.save()

def filter_user_account(user, account_id):
    try:
        account = Account.objects.filter(user=user).get(pk=account_id)
    except Exception as ex:
        print(ex)
        raise ValueError("No such account")
    return account


def book_exists(book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Exception as ex:
        print(ex)
        raise ValueError("No such book")
    return book

def cart_exists(cart_id):
    try:
        cart = Cart.objects.get(pk=cart_id)
    except Exception as ex:
        print(ex)
        raise ValueError("No such book")
    return cart
