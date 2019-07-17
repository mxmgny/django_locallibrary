from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_genre_novel = Genre.objects.filter(name__icontains='novel').count()
    num_books_war = Book.objects.filter(title__icontains='war').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_novel': num_genre_novel,
        'num_books_war': num_books_war,
    }

    return render(request, 'index.html', context=context)
