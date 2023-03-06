from .serializer import BookSerializer, CustomerSerializer, AccountSerializer, DepositSerializer, OrderSerializer, BookDetailSerializer
from .models import Book, Customer, Account, Deposit, Order
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .actions import make_order, filter_user_account, book_exists


class BookViewList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


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
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()

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


class OrderView(APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        account = filter_user_account(
            self.request.user, self.request.data['customer'])

        book = book_exists(self.request.data['book'])
        make_order(account, book)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        orders = Order.objects.filter(customer=request.user.id)
        count = len(orders)
        if count == 0:
            return Response({"message": "You haven't made any orders yet"})
        else:
            serializer = OrderSerializer(orders, many=True)
            latest_id = serializer.data[-1].get('id')
            latest_order = orders.get(pk=latest_id)
            latest_order_serializer = OrderSerializer(latest_order)
            return Response({"Your last order": latest_order_serializer.data})


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user.id)