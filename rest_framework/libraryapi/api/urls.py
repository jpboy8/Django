from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import BookViewList, BookDetailView, CustomerInfoView, AccountView, DepositView, OrderView, OrderListView, RegisterUserView,CartViewSet,CartItemViewSet,CartOrderView

router = routers.DefaultRouter()
router.register("carts", CartViewSet)

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('books/', BookViewList.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('customer/', CustomerInfoView.as_view()),
    path('account/', AccountView.as_view()),
    path('deposit/', DepositView.as_view()),
    path('order/', OrderView.as_view()),
    path('order-list', OrderListView.as_view()),
    path('order-cart/', CartOrderView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path("", include(cart_router.urls)),
    path("", include(router.urls))
]
