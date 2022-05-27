from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date
import uuid
from tinymce.models import HTMLField


class Genre(models.Model):
    name = models.CharField(_('pavadinimas'), max_length=200, help_text=_('įveskite knygos žanrą (pvz. detektyvas)'))

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(_('vardas'), max_length=100)
    last_name = models.CharField(_('pavardė'), max_length=100)
    description = HTMLField(_('apie autorių'), blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_books_count(self):
        return self.books.count()
    get_books_count.short_description = _('knygos')

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('autorius')
        verbose_name_plural = _('autoriai')


class Book(models.Model):
    title = models.CharField(_('pavadinimas'), max_length=250)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name=_('autorius'))
    summary = HTMLField(_('santrauka'), help_text=_('trumpas knygos aprašymas'))
    isbn = models.CharField('ISBN', max_length=13, help_text=_('13 Simbolių')+'<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">'+_('ISBN kodas')+'</a>')
    genre = models.ManyToManyField(Genre, verbose_name=_('žanras'), help_text='išrinkite žanrą(-us) šiai knygai')
    cover = models.ImageField(_('viršelis'), upload_to='books/covers', null=True, blank=True)

    def __str__(self):
        return f'{str(self.author)} - {self.title}'

    def display_genres(self):
        return ', '.join(genre.name for genre in self.genre.all()[:7])
    display_genres.short_description = _('žanrai')

    def get_available_instances(self):
        return self.book_instances.filter(status__exact='g').count()
    get_available_instances.short_description = _('prieinamų kopijų kiekis')


class BookInstance(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, help_text=_('unikalus ID knygos kopijai'), editable=False)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book_instances', verbose_name=_('knyga'))
    due_back = models.DateField(_('grąžinama'), null=True, blank=True, db_index=True)

    LOAN_STATUS = (
        ('a', _('administruojama')),
        ('p', _('paimta')),
        ('g', _('galima paimti')),
        ('r', _('rezervuota')),
    )

    status = models.CharField(_('statusas'), max_length=1, choices=LOAN_STATUS, blank=True, default='a', db_index=True)
    reader = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='book_instances', 
        verbose_name=_('skaitytojas'), 
        null=True, 
        blank=True,
    )

    def __str__(self):
        return f'{str(self.id)} - {self.book.title}'

    @property
    def is_overdue(self):
        if self.due_back and self.due_back < date.today():
            return True
        return False

    class Meta:
        ordering = ['due_back']
        verbose_name = _('knygos kopija')
        verbose_name_plural = _('knygos kopijos')


class BookReview(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='book_reviews', 
        verbose_name=_('knyga'),
        null=True,
        blank=True,
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='book_reviews',
        verbose_name=_('skaitytojas'),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = HTMLField('atsiliepimas')

    def __str__(self):
        return f'{self.book} - {self.reviewer} - {self.created_at}'
