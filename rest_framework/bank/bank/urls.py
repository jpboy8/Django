from django.urls import path
from .views import CustomerInfo, AccountInfo, DepositView, TransferView


urlpatterns = [
    path('customer/', CustomerInfo.as_view()),
    path('account/', AccountInfo.as_view()),
    path('deposit/', DepositView.as_view()),
    path('transfer/', TransferView.as_view()),
]
