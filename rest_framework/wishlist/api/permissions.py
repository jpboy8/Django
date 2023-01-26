from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # override has_object_permission method to check if the user is a owner of wishlist
    def has_object_permission(self, request, view, obj):
        if str(type(obj)) == "<class 'api.models.Wishlist'>":
            return obj.author == request.user
        else:
            return obj.wishlist.author == request.user
