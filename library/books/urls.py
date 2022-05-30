from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('my_books/', views.LoanedBooksByUser.as_view(), name='my_books'),
    path('my_book/<uuid:pk>/', views.BookByUserDetailView.as_view(), name='my_book'),
    path('my_book/new/', views.BookByUserCreateView.as_view(), name="my_book_new"),
    path('my_book/<uuid:pk>/update/', views.BookByUserUpdateView.as_view(), name='my_book_update'),
    path('my_book/<uuid:pk>/delete/', views.BookByUserDeleteView.as_view(), name='my_book_delete'),
]
