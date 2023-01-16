from django.urls import path
from .views import BookViewList, BookDetailView

urlpatterns = [
    path('books/', BookViewList.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
]