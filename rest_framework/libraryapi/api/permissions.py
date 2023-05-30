from rest_framework.permissions import IsAuthenticated

class IsNotAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
