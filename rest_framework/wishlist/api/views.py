from .models import Wishlist, Item
from .serializer import WishlistSerializer, ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner
from django.shortcuts import get_object_or_404

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
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data)


class CreateItemView(APIView):
    serializer_class = ItemSerializer
    permission_classes = (IsOwner, )

    def get(self, request, *args, **kwargs):
        data = Item.objects.filter(wishlist=kwargs.get('pk'))
        global wishlist_id
        wishlist_id = int(kwargs.get('pk'))
        # take wishlist object to check permission
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        # check permission, because without it permisson_classes doesnt work
        self.check_object_permissions(request, wishlist)
        if wishlist_id > len(Wishlist.objects.all()):
            return Response({'error': '404'}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            data, many=True, context={'request': wishlist_id})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        w = Wishlist.objects.get(id=kwargs.get('pk'))
        serializer.save(wishlist=w)

        return Response(serializer.data)
