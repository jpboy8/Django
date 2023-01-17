from .models import Book, Customer, Account, Deposit
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
            self.fields['account'] = self.fields['account']\
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
