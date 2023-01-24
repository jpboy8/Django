from django.urls import path
from .views import WishlistView

urlpatterns = [
    path('wishlists/', WishlistView.as_view())
]
