from django.urls import path
from .views import BookViewList, BookDetailView, CustomerInfoView, AccountView, DepositView

urlpatterns = [
    path('books/', BookViewList.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('customer/', CustomerInfoView.as_view()),
    path('account/', AccountView.as_view()),
    path('deposit/', DepositView.as_view()),
]
