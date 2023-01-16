from .models import Account, Transfer
from django.db import transaction
from django.core.exceptions import ValidationError


def make_transfer(from_account, to_account, amount):
    if from_account.balance < amount:
        raise ValidationError('Not enough money')

    if from_account == to_account:
        raise ValidationError('Choose anoter account')

    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()

        transfer = Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

    return transfer


def filter_user_account(user, account_id):
    try:
        account = Account.objects.filter(user=user).get(pk=account_id)
    except (Account.DoesNotExist):
        raise ValueError('Account does not exist')

    return account


def check_account_exists(account_id):
    try:
        account = Account.objects.get(pk=account_id)
        print(account)
    except Exception as e:
        print(e)
        raise ValueError('No such account')
    return account
