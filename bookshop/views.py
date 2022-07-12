from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import (
    ListView,
    DetailView, FormView,
)

from .models import (
    Category,
    Subcategory,
    Book,
    Review,
    LikeReview, DislikeReview, CustomerOrder, Author, Publisher, BookSeries,
)

from .forms import CustomerOrderForm, RegistrationUserForm, LoginUserForm
from cart.cart import Cart
from .utilities import user_is_active


class BookListView(ListView):
    template_name = 'bookshop/index.html'
    model = Book
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        cart = Cart(self.request)
        context['book_in_cart'] = cart.get_book_ids()
        context = context | user_is_active(self.request)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'bookshop/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['subcategory_list'] = kwargs['object'].subcategory.all()
        context = context | user_is_active(self.request)
        return context


class SubCategoryDetailView(DetailView):
    model = Subcategory
    template_name = 'bookshop/subcategory_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['object_list'] = Book.objects.filter(category=kwargs['object'])
        context['by_category'] = kwargs['object']
        cart = Cart(self.request)
        context['book_in_cart'] = cart.get_book_ids()
        context = context | user_is_active(self.request)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshop/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['topical_category'] = Category.objects.get(subcategory=kwargs['object'].category)
        review_list = Review.objects.filter(book=kwargs['object'])
        paginator = Paginator(review_list, 2)
        page_number = self.request.GET.get('page')
        context['paginator'] = paginator
        context['reviews'] = paginator.get_page(page_number)
        context = context | user_is_active(self.request)
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'bookshop/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Book.objects.filter(author=kwargs['object'])
        paginator = Paginator(object_list, 2)
        page_number = self.request.GET.get('page')
        context['paginator'] = paginator
        context['object_list'] = paginator.get_page(page_number)
        context['category_list'] = Category.objects.all()
        context = context | user_is_active(self.request)
        return context


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'bookshop/publisher_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Book.objects.filter(publisher=kwargs['object'])
        paginator = Paginator(object_list, 2)
        page_number = self.request.GET.get('page')
        context['paginator'] = paginator
        context['object_list'] = paginator.get_page(page_number)
        context['category_list'] = Category.objects.all()
        context = context | user_is_active(self.request)
        return context


class BookSeriesDetailView(DetailView):
    model = BookSeries
    template_name = 'bookshop/bookseries_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Book.objects.filter(book_series=kwargs['object'])
        paginator = Paginator(object_list, 2)
        page_number = self.request.GET.get('page')
        context['paginator'] = paginator
        context['object_list'] = paginator.get_page(page_number)
        context['category_list'] = Category.objects.all()
        context = context | user_is_active(self.request)
        return context


@login_required(login_url='/booklover/login')
def like_review(request, pk):
    like, dislike = request.POST.get('like'), request.POST.get('dislike')
    review = Review.objects.get(pk=pk)

    if like:
        is_like = LikeReview.objects.get_or_none(user=request.user, review=review)
        if is_like:
            is_like.delete()
        else:
            check_dislike = DislikeReview.objects.get_or_none(user=request.user, review=review)
            if check_dislike:
                check_dislike.delete()
            LikeReview.objects.update_or_create(user=request.user, review=review)
    elif dislike:
        is_dislike = DislikeReview.objects.get_or_none(user=request.user, review=review)
        if is_dislike:
            is_dislike.delete()
        else:
            check_like = LikeReview.objects.get_or_none(user=request.user, review=review)
            if check_like:
                check_like.delete()
            DislikeReview.objects.update_or_create(user=request.user, review=review)

    return HttpResponseRedirect(reverse('book_detail', args=(review.book.pk,)))


class OrderingCreateView(FormView):
    form_class = CustomerOrderForm
    template_name = 'bookshop/ordering.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        data = self.request.session.get('ordering_data')
        context['data'] = data
        context = context | user_is_active(self.request)
        return context

    def post(self, request, *args, **kwargs):
        order_data = request.session['ordering_data'] = {}
        order_data['mail'] = request.POST.get('mail')
        order_data['city'] = request.POST.get('city')
        order_data['post_department'] = request.POST.get('post_department')
        order_data['phone_number'] = request.POST.get('phone_number')
        order_data['session_key'] = request.session.__dict__.get('_SessionBase__session_key')
        return super().post(request)

    def get_success_url(self):
        return reverse('payment:pay_view')


class RegistrationUser(FormView):
    template_name = 'bookshop/register_page.html'
    form_class = RegistrationUserForm
    success_url = '/booklover/login/'

    def form_valid(self, form):
        cd = form.cleaned_data
        username, email, password = (
            cd['username'],
            cd['email'],
            cd['password'],
        )
        User.objects.create_user(username=username, email=email, password=password)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = context | user_is_active(self.request)
        context['category_list'] = Category.objects.all()
        return context


class LoginUser(FormView):
    template_name = 'bookshop/login_page.html'
    form_class = LoginUserForm
    success_url = '/booklover/'

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context | user_is_active(self.request)
        context['category_list'] = Category.objects.all()
        return context


def logout_view(request):
    logout(request)
    return redirect('/booklover/')


def personal_account(request):
    order_list = CustomerOrder.objects.filter(user=User.objects.get(pk=request.user.pk))
    context = {'order_list': order_list}
    context = context | user_is_active(request)
    context['category_list'] = Category.objects.all()
    return render(request, 'bookshop/personal_account.html', context)


class CustomerOrderDetail(DetailView):
    model = CustomerOrder
    template_name = 'bookshop/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context | user_is_active(self.request)
        context['category_list'] = Category.objects.all()
        return context
