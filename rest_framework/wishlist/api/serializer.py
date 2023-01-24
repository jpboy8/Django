from rest_framework import serializers
from .models import Wishlist, Item
from django.contrib.auth.models import User


class WishlistSerializer(serializers.ModelSerializer):
    # to limit choices of authors in browsable api
    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['author'].queryset = User._default_manager.filter(
                pk=self.context['request'].user.id)

    class Meta:
        fields = ['id', 'title', 'author']
        model = Wishlist
        read_only_fields = ['id', ]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'wishlist', 'name', 'description', 'date']
        read_only_fields = ['id']
        model = Item
