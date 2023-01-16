from rest_framework import serializers
from .models import Customer, Account, Deposit, Transfer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'city', 'email', 'phone')
        model = Customer
        read_only_fields = ['id']

    def create(self, validated_data):
        # override standard method to create customer without pk in url
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'balance')
        model = Account
        read_only_fields = ['id', 'balance']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return Account(**validated_data)


class DepositSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DepositSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user.id)

    class Meta:
        fields = ('id', 'amount', 'date', 'account')
        model = Deposit
        read_only_fields = ['id', 'date']

    def create(self, validated_data):
        if validated_data['account'].balance + validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError(
                ('Not enough money')
            )

        return super(DepositSerializer, self).create(validated_data)


class TransferSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account']\
                .queryset.filter(user=self.context['view'].request.user.id)

    def validate(self, data):
        try:
            data['to_account'] = Account.objects.get(pk=data['to_account'].id)
        except Exception as ex:
            print(ex)
            raise serializers.ValidationError(
                "No such account from serializer"
            )
        return data

    class Meta:
        fields = ('id', 'from_account', 'to_account', 'amount')
        model = Transfer
        read_only_fields = ['id']
