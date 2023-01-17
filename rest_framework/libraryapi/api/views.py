from .serializer import BookSerializer, CustomerSerializer, AccountSerializer, DepositSerializer
from .models import Book, Customer, Account, Deposit
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class BookViewList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CustomerInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user.id).first()


class AccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user.id).first()


class DepositView(APIView):
    def post(self, request, *args, **kwargs):
        DepositSerializer(data=request.data).is_valid(raise_exception=True)
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = Account.objects.filter(
                user=request.user.id).get(pk=request.data['account'])
        except Exception as ex:
            print(ex)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(account=account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        deposits = Deposit.objects.filter(account=request.user.id)
        count = len(deposits)
        if count == 0:
            return Response({"message": "You haven't made any deposits yet"})
        else:    
            serializer = DepositSerializer(deposits, many=True)
            latest_id = serializer.data[-1].get('id')
            latest_deposit = deposits.get(pk=latest_id)
            latest_dep_serializer = DepositSerializer(latest_deposit)
            return Response({"Your last deposit": latest_dep_serializer.data})
