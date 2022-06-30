from bookshop.models import Book


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            self.session['cart'] = {}
        else:
            self.session['cart'] = cart

        self.cart = self.session['cart']

    def add(self, book_pk):
        current_book = Book.objects.get(pk=book_pk)
        current_book.in_cart = True
        current_book.save()
        self.cart[str(book_pk)] = {'quantity': 1, 'price': current_book.price}

    def update_quantity(self, pk, var):
        self.cart[str(pk)]['quantity'] += var

    def clear(self):
        del self.session['cart']
        self.session.modified = True

    def remove(self, pk):
        del self.session['cart'][str(pk)]
        self.session.modified = True

    def get_book_ids(self):
        return [int(i) for i in self.cart]
