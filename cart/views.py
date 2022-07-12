from django.shortcuts import render, redirect

from bookshop.models import Book, Category
from bookshop.utilities import user_is_active
from .cart import Cart


def cart_add(request, **kwargs):
    cart = Cart(request)
    cart.add(kwargs['pk'])

    return redirect('cart:open_cart')


def open_cart(request):
    cart = Cart(request)

    if request.method == 'GET':
        if 'add' in request.GET:
            cart.update_quantity(request.GET.get('add'), 1)
            return redirect('cart:open_cart')
        elif 'remove' in request.GET:
            cart.update_quantity(request.GET.get('remove'), -1)
            return redirect('cart:open_cart')

    books_ids = cart.cart.keys()
    object_list = Book.objects.filter(pk__in=books_ids)

    display_cart = {}

    for i in range(len(books_ids)):
        current_book = object_list[i]
        display_cart[str(current_book.pk)] = {
            'current_book': current_book,
            'quantity': cart.cart[str(current_book.pk)]['quantity'],
            'total_price': cart.cart[str(current_book.pk)]['quantity'] * cart.cart[str(current_book.pk)]['price']
        }

        if display_cart[str(current_book.pk)]['quantity'] <= 1:
            display_cart[str(current_book.pk)]['is_one'] = True
        else:
            display_cart[str(current_book.pk)]['is_one'] = False

    total_price = 0
    for value in display_cart.values():
        total_price += value['total_price']

    context = {
        'display_cart': display_cart,
        'books_ids': books_ids,
        'total_price': total_price,
        'category_list': Category.objects.all(),
    }
    context = context | user_is_active(request)
    return render(request, 'bookshop/cart.html', context)


def clear_cart(request):
    cart = Cart(request)
    cart.clear()

    return redirect('cart:open_cart')


def remove_from_cart(request, pk):
    cart = Cart(request)
    cart.remove(pk)

    return redirect('cart:open_cart')