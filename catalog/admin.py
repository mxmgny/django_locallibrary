from django.contrib import admin
from .models import Author, Language, Book, BookInstance, Genre
# Register your models here.


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'due_back')
    list_filter = ( 'status', 'due_back',)

    fieldsets = (
        ('Instance', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Avaliability', {
            'fields': ('status', 'due_back')
        })
    )


admin.site.register(Language)
admin.site.register(Genre)
