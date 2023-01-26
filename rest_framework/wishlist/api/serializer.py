from rest_framework import serializers
from .models import Wishlist, Item
from django.contrib.auth.models import User


class WishlistSerializer(serializers.ModelSerializer):
    # to limit choices of authors in browsable api
    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            print(type(self.context['request'].user))
            self.fields['author'].queryset = User._default_manager.filter(
                pk=self.context['request'].user.id)

    class Meta:
        fields = ['id', 'title', 'author']
        model = Wishlist
        read_only_fields = ['id', ]


class ItemSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ItemSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            # get pk of wishlist
            wishlist_id = kwargs.get('context').get('request')
            str_n = str(wishlist_id)
            # get integer from kwargs.get('context').get('request')
            for i in str_n:
                if i.isdigit():
                    wishlist_id = int(i)

            # limit choices of wishlists in browsable api
            self.fields['wishlist'].queryset = Wishlist._default_manager\
                .filter(pk=wishlist_id)

    class Meta:
        fields = ['id', 'wishlist', 'name', 'description', 'date']
        read_only_fields = ['id']
        model = Item
