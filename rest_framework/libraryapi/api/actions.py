from .models import Account, Book
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
