from django.db import models
import uuid


class Genre(models.Model):
    name = models.CharField('pavadinimas', max_length=200, help_text='įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField('vardas', max_length=100)
    last_name = models.CharField('pavardė', max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'autorius'
        verbose_name_plural = 'autoriai'


class Book(models.Model):
    title = models.CharField('pavadinimas', max_length=250)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name='autorius')
    summary = models.TextField('santrauka', max_length=1000, help_text='trumpas knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN kodas</a>')
    genre = models.ManyToManyField(Genre, verbose_name='žanras', help_text='išrinkite žanrą(-us) šiai knygai')

    def __str__(self):
        return f'{str(self.author)} - {self.title}'


class BookInstance(models.Model):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, help_text='unikalus ID knygos kopijai')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book_instances', verbose_name='knyga')
    due_back = models.DateField('grąžinama', null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'administruojama'),
        ('p', 'paimta'),
        ('g', 'galima paimti'),
        ('r', 'rezervuota'),
    )

    status = models.CharField('statusas', max_length=1, choices=LOAN_STATUS, blank=True, default='a')

    def __str__(self):
        return f'{str(self.id)} - {self.book.title}'

    class Meta:
        ordering = ['due_back']
        verbose_name = 'knygos kopija'
        verbose_name_plural = 'knygos kopijos'
