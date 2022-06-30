from django.views.generic import (
    ListView,
    DetailView,
)

from .models import (
    Category,
    Subcategory,
    Book,
)

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
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshop/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context
