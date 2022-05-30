from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from .forms import BookReviewForm
from .models import Book, Author, BookInstance


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }

    return render(request, 'books/index.html', context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 5)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)
    return render(request, 'books/authors.html', {'authors': authors})


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'books/author.html', {'author': author})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    # queryset = Book.objects.filter(title__icontains=':')[:5:1]
    template_name = 'books/book_list.html'
    extra_context = {'spalva': '#fc0'}
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(author__last_name__istartswith=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = {} # this and below line technically repeats the above
        # context.update({self.context_object_name: self.get_queryset()})
        context.update({'spalva': 'wheat'}) #overwrites self.extra_context if matched as well
        return context


class BookDetailView(generic.DetailView, FormMixin):
    model = Book
    template_name = 'books/book_detail.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id })
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


class LoanedBooksByUser(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'books/user_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(reader=self.request.user).filter(Q(status__exact='p') | Q(status__exact='r')).order_by('due_back')


class BookByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'books/user_book_detail.html'


class BookByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    fields = ('book', 'due_back', )
    success_url = reverse_lazy('my_books')
    template_name = 'books/user_book_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['book'] = self.request.GET.get('book_id')
        initial['due_back'] = date.strftime(date.today() + timedelta(days=14), '%Y-%m-%d')
        return initial

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'r'
        return super().form_valid(form)


class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    fields = ('book', 'due_back', )
    success_url = reverse_lazy('my_books')
    template_name = 'books/user_book_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'p'
        return super().form_valid(form)

    def test_func(self):
        book_instance = self.get_object()
        return book_instance.reader == self.request.user
