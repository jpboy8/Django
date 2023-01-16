from .models import Customer, Account, Deposit, Transfer
from .serializer import CustomerSerializer, AccountSerializer, DepositSerializer, TransferSerializer
from rest_framework import generics, viewsets, mixins
from rest_framework import permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import make_transfer, filter_user_account, check_account_exists
import decimal
# from .services import make_transfer, filter_user_account, check_account_exists


class CustomerInfo(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(user=self.request.user.id).first()


class AccountInfo(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(user=self.request.user.id).first()


class DepositView(generics.ListCreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Deposit.objects.all()

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user.id)
        count = len(self.queryset.filter(account__in=accounts))
        return self.queryset.filter(id=count)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = Account.objects.filter(
                user=self.request.user.id).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class TransferView(APIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transfer.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        from_account = filter_user_account(
            self.request.user,
            self.request.data['from_account'])

        # to_account = check_account_exists(self.request.data['to_account'])
        to_account = Account.objects.get(pk=self.request.data['to_account'])
        make_transfer(
            from_account,
            to_account,
            decimal.Decimal(self.request.data['amount']))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
