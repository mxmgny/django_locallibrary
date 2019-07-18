from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre_novel = Genre.objects.filter(name__icontains='novel').count()
    num_books_war = Book.objects.filter(title__icontains='war').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_novel': num_genre_novel,
        'num_books_war': num_books_war,
        'num_visits':num_visits
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(ListView):
    """ View to display all the books in library """
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 5


class BookDetailView(DetailView):
    """View to display book detail information and book instances"""
    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorListView(ListView):
    model = Author
    paginate_by = 5
    template_name = 'catalog/author_list.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
