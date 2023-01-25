from django.urls import path
from .views import WishlistView, CreateItemView

urlpatterns = [
    path('wishlists/', WishlistView.as_view()),
    path('wishlists/<int:pk>/', CreateItemView.as_view()),
]
