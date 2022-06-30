from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField('Назва категорії', max_length=50)
    subcategory = models.ManyToManyField('Subcategory', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', args=(self.pk,))


class Subcategory(models.Model):
    title = models.CharField('*Назва підкатегорії', max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subcategory_detail', args=(self.pk,))


class Book(models.Model):
    LANGUAGE = (
        ('українська', 'Українська'),
        ('російська', 'Російська'),
        ('англійська', 'Англійська')
    )

    ILLUSTRATIONS = (
        ('чорно-білі', 'Чорно-білі'),
        ('багатокольорові', 'Багатокольорові'),
        ('без зображень', 'Без зображень')
    )

    PALETTE = (
        ('тверда', 'Тверда'),
        ("м'яка", "М'яка")
    )

    PAPER = (
        ('офсетний', 'Офсетний'),
        ('мелований', 'Мелований'),
    )

    BOOK_TYPE = (
        ('паперова', 'Паперова'),
        ('електронна', 'Електронна')
    )

    author = models.ManyToManyField(
        'Author',
        verbose_name='Автор',
        blank=True,
        default='Не обрано'
    )

    interpreter = models.ManyToManyField(
        'Interpreter',
        verbose_name='Перекладач',
        blank=True,
        default='Не обрано',
    )

    illustrator = models.ManyToManyField(
        'Illustrator',
        verbose_name='Ілюстратор',
        blank=True,
        default='Не обрано',
    )

    publisher = models.ForeignKey(
        'Publisher',
        verbose_name='*Видавництво',
        on_delete=models.SET_DEFAULT,
        default='Не обрано'
    )

    book_series = models.ForeignKey(
        'BookSeries',
        verbose_name='Серія книг',
        on_delete=models.SET_DEFAULT,
        default='Не обрано',
        blank=True
    )

    category = models.ForeignKey(
        'Subcategory',
        verbose_name='Категорія',
        on_delete=models.SET_DEFAULT,
        default='Не обрано',
        blank=True
    )

    edition = models.IntegerField(verbose_name='Тираж', blank=True, null=True)
    weight = models.IntegerField(verbose_name='Вага', blank=True, null=True)
    first_publication_year = models.IntegerField(verbose_name='Рік першого видання', blank=True, null=True)

    price = models.IntegerField(verbose_name='*Ціна')
    publication_year = models.IntegerField(verbose_name='*Рік видання')
    page_count = models.IntegerField(verbose_name='*Кількість сторінок')

    language = models.CharField(choices=LANGUAGE, max_length=15, verbose_name='*Мова')
    palette = models.CharField(choices=PALETTE, max_length=30, verbose_name='*Палітурка')
    paper = models.CharField(choices=PAPER, max_length=30, verbose_name='*Папір')
    book_type = models.CharField(choices=BOOK_TYPE, max_length=30, verbose_name='*Тип')

    Illustrations = models.CharField(choices=ILLUSTRATIONS, max_length=25, verbose_name='Ілюстрації', blank=True,
                                     null=True)

    title = models.CharField('*Назва книги', null=True, max_length=100)
    format = models.CharField('*Формат книги (приклад: 145х215 мм)', max_length=100)
    isbn = models.CharField('*isbn', max_length=25)
    code_product = models.CharField('*Код товару', max_length=9)

    cover_photo = models.ImageField('*Фото', upload_to='img')

    def __str__(self):
        return f'{self.title}: ({self.code_product})'

    def get_absolute_url(self):
        return reverse('book_detail', args=(self.pk,))


class Author(models.Model):
    name = models.CharField("*Ім'я автора", max_length=100)

    birthdate = models.DateField('Дата народження', blank=True, null=True)
    death_date = models.DateField('Дата смерті', blank=True, null=True)
    biography = models.TextField('Біографія', blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    title = models.CharField('*Назва видавництва', max_length=100)
    photo = models.ImageField('*Фото', upload_to='img')
    info = models.TextField('*Опис видавництва')

    def __str__(self):
        return self.title


class BookSeries(models.Model):
    title = models.CharField('*Серія книг', max_length=100)

    def __str__(self):
        return self.title


class Interpreter(models.Model):
    title = models.CharField('*Перекладач', max_length=100)

    def __str__(self):
        return self.title


class Illustrator(models.Model):
    title = models.CharField('*Ілюстратор', max_length=100)

    def __str__(self):
        return self.title
