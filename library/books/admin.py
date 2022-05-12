from django.contrib import admin
from .models import Author, Book, BookInstance, Genre


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genres', )
    inlines = (BookInstanceInline, )


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', )
    list_filter = ('status', 'due_back', )

    fieldsets = (
        ('Pagrindinė Informacija', {'fields': (
                'id', 
                'book', 
            )}),
        ('Prieinamumas', {'fields': (
                'status', 
                'due_back', 
            )}),
    )


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)
