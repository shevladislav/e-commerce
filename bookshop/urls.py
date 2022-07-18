from django.urls import path

from .views import (
    BookListView,
    CategoryDetailView,
    SubCategoryDetailView,
    BookDetailView,
    OrderingCreateView,
    AuthorDetailView,
    like_review,
    RegistrationUser,
    LoginUser,
    personal_account,
    CustomerOrderDetail,
    logout_view,
    PublisherDetailView,
    BookSeriesDetailView,
    form_review,
)

urlpatterns = [
    path('', BookListView.as_view(), name='home_page'),
    path('category-detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategory-detail/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book-detail-like/<int:pk>/', like_review, name='like_review'),
    path('author-detail/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('publisher-detail/<int:pk>/', PublisherDetailView.as_view(), name='publisher_detail'),
    path('bookseries-detail/<int:pk>/', BookSeriesDetailView.as_view(), name='bookseries_detail'),
    path('ordering/', OrderingCreateView.as_view(), name='ordering_view'),
    path('registration/', RegistrationUser.as_view(), name='registration_view'),
    path('login/', LoginUser.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('personal-account/', personal_account, name='personal_account'),
    path('order-detail/<int:pk>/', CustomerOrderDetail.as_view(), name='order_detail'),
    path('form-review/<int:pk>/', form_review, name='review_form'),
]
