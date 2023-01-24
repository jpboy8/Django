from .models import Wishlist, Item
from .serializer import WishlistSerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class WishlistView(APIView):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()

    def get(self, request, *args, **kwargs):
        data = Wishlist.objects.filter(author=request.user.id)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data)
