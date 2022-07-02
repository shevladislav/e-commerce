from django.urls import reverse

from django.views.generic import (
    ListView,
    DetailView, FormView,
)

from .models import (
    Category,
    Subcategory,
    Book,
)

from .forms import CustomerOrderForm
from cart.cart import Cart


class BookListView(ListView):
    template_name = 'bookshop/index.html'
    model = Book
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        cart = Cart(self.request)
        context['book_in_cart'] = cart.get_book_ids()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'bookshop/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['subcategory_list'] = kwargs['object'].subcategory.all()
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
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshop/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class OrderingCreateView(FormView):
    form_class = CustomerOrderForm
    template_name = 'bookshop/ordering.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        data = self.request.session.get('ordering_data')
        context['data'] = data
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
