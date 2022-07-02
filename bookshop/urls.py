from django.urls import path

from .views import (
    BookListView,
    CategoryDetailView,
    SubCategoryDetailView,
    BookDetailView,
    OrderingCreateView
)

urlpatterns = [
    path('', BookListView.as_view(), name='home_page'),
    path('category-detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategory-detail/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('ordering/', OrderingCreateView.as_view(), name='ordering_view'),
]
