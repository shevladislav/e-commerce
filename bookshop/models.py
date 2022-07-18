from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
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
    rating = models.IntegerField(verbose_name='Рейтинг', default=0, blank=True, null=True)

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

    description = models.TextField(null=True, verbose_name='Усе про книжку')

    def __str__(self):
        return f'{self.title}: ({self.code_product})'

    def get_absolute_url(self):
        return reverse('book_detail', args=(self.pk,))

    def average_rating(self):
        review_list = [int(i.rating) for i in Review.objects.filter(book=self)]
        rating = sum(review_list) / len(review_list)
        return int(rating)

    def absolute_average_rating(self):
        review_list = [int(i.rating) for i in Review.objects.filter(book=self)]
        rating = sum(review_list) / len(review_list)
        return round(rating, 1)

    def get_rating_by_grade(self):
        review_list = [int(i.rating) for i in Review.objects.filter(book=self)]
        length = len(review_list)
        star_1, star_2, star_3, star_4, star_5 = [True for star in review_list if star in (1,)], \
                                                 [True for star in review_list if star in (2,)], \
                                                 [True for star in review_list if star in (3,)], \
                                                 [True for star in review_list if star in (4,)], \
                                                 [True for star in review_list if star in (5,)]
        star_1, star_2, star_3, star_4, star_5 = sum(star_1) * 100 // length, \
                                                 sum(star_2) * 100 // length, \
                                                 sum(star_3) * 100 // length, \
                                                 sum(star_4) * 100 // length, \
                                                 sum(star_5) * 100 // length

        return star_1, star_2, star_3, star_4, star_5

    def count_review(self):
        review_list = ['.' for i in Review.objects.filter(book=self)]
        return len(review_list)


class Author(models.Model):
    name = models.CharField("*Ім'я автора", max_length=100)

    birthdate = models.DateField('Дата народження', blank=True, null=True)
    death_date = models.DateField('Дата смерті', blank=True, null=True)
    biography = models.TextField('Біографія', blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail', args=(self.pk,))


class Publisher(models.Model):
    title = models.CharField('*Назва видавництва', max_length=100)
    photo = models.ImageField('*Фото', upload_to='img')
    info = models.TextField('*Опис видавництва')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publisher_detail', args=(self.pk,))


class BookSeries(models.Model):
    title = models.CharField('*Серія книг', max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookseries_detail', args=(self.pk,))


class Interpreter(models.Model):
    title = models.CharField('*Перекладач', max_length=100)

    def __str__(self):
        return self.title


class Illustrator(models.Model):
    title = models.CharField('*Ілюстратор', max_length=100)

    def __str__(self):
        return self.title


class CustomerOrder(models.Model):
    order_items = models.TextField()
    mail = models.CharField(max_length=100, verbose_name='Електронна пошта')
    city = models.CharField(max_length=100, verbose_name='Місто доставки')
    post_department = models.CharField(max_length=150, verbose_name='Поштове відділення(номер, адреса)')
    phone_number = models.CharField(max_length=15, null=True, verbose_name='Номер телефона')
    status_success = models.BooleanField(null=True)
    total_price = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.date}'

    def get_absolute_url(self):
        return reverse('order_detail', args=(self.pk,))


class Review(models.Model):
    RATING = (
        ('1', 'Жахливо'),
        ('2', 'Погано'),
        ('3', 'Середньо'),
        ('4', 'Добре'),
        ('5', 'Чудово')
    )

    title = models.CharField('Заголовок', max_length=100)
    body = models.TextField('Рецензія', max_length=2500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.CharField('Рейтинг', choices=RATING, max_length=100)


    def __str__(self):
        return f'{self.user}: {self.title}'

    def count_like(self):
        like_list = LikeReview.objects.filter(review=self)
        return len(like_list)

    def count_dislike(self):
        like_list = DislikeReview.objects.filter(review=self)
        return len(like_list)


class LikeDislikeManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class LikeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    objects = LikeDislikeManager()


class DislikeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    objects = LikeDislikeManager()