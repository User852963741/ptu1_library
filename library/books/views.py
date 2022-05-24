from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from .models import Book, Author, BookInstance


@csrf_protect
def register(request):
    context = None
    if request.method == "POST":
        # duomenu surinkimas
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validuosim forma, tikrindami ar sutampa slaptažodžiai, ar egzistuoja vartotojas
        error = False
        if not password or password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa arba neįvesti.')
            error = True
        if not username or User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojas {username} jau egzistuoja arba neįvestas.')
            error = True
        if not email or User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el.praštu {email} jau egzistuoja arba neįvestas.')
            error = True
        if error:
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'Vartotojas {username} užregistruotas sėkmingai. Galite prisijungti')
            return redirect('index')
    return render(request, 'books/register.html')


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


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class LoanedBooksByUser(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'books/user_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(reader=self.request.user).filter(Q(status__exact='p') | Q(status__exact='r')).order_by('due_back')
