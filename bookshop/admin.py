from django.contrib import admin

from .models import (
    Category,
    Subcategory,
    Book,
    BookSeries,
    Publisher,
    Author,
    Interpreter,
    Illustrator,
    CustomerOrder,
    Review,
)

admin.site.register(Review)
admin.site.register(CustomerOrder)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(BookSeries)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Interpreter)
admin.site.register(Illustrator)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    filter_horizontal = ['author', 'interpreter', 'illustrator']
    list_filter = ['author', 'interpreter', 'illustrator', 'publisher', 'book_series']
    list_display = ['title', 'code_product', 'isbn']
    search_fields = ['title', 'code_product', 'isbn']
    list_per_page = 7
