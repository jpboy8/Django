from .serializer import BookSerializer, CustomerSerializer, AccountSerializer, DepositSerializer, OrderSerializer, BookDetailSerializer,UserSerializer,CartSerializer, CartItemSerializer,AddCartItemSerializer, UpdateCartItemSerializer, CartOrderSerializer, OrderListSerializer
from .models import Book, Customer, Account, Deposit, Order, Cart, Cartitems,CartOrder
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .actions import make_order, filter_user_account, book_exists, make_order_cart,cart_exists
from .permissions import IsNotAuthenticated
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend


class RegisterUserView(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsNotAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BookViewList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['title','author']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author', 'price']

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
    serializer_class = OrderListSerializer
    def get_queryset(self):
        print(self.request.user.id)
        print(Order.objects.filter(customer=6))
        acc = Account.objects.get(user=self.request.user.id)
        print(Account.objects.get(user=self.request.user.id))
        print(acc.id)
        
        return Order.objects.filter(customer=acc.id)



class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request):
        acc = Account.objects.get(user=self.request.user.id)
        carts = Cart.objects.filter(owner=acc.id)
        serializer = self.serializer_class(carts, many=True)
        return Response(serializer.data)


class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer 
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}
    
    
class CartOrderView(generics.ListCreateAPIView):
    serializer_class = CartOrderSerializer

    def get_queryset(self):
        return CartOrder.objects.filter(customer=self.request.user.id)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        account = filter_user_account(
            self.request.user, self.request.data['customer'])

        cart = cart_exists(self.request.data['cart'])
        make_order_cart(account, cart)
        serializer.save()
        return Response(serializer.data)