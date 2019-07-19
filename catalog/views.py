import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Book, BookInstance, Author, Genre
from .forms import RenewBookForm

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre_novel = Genre.objects.filter(name__icontains='novel').count()
    num_books_war = Book.objects.filter(title__icontains='war').count()
    print(request.user.get_all_permissions())
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_novel': num_genre_novel,
        'num_books_war': num_books_war,
        'num_visits': num_visits
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(ListView):
    """ View to display all the books in library """
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.all().order_by('title')


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


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)\
            .filter(status__exact='o')\
            .order_by('due_back')


class LoanedBooksStuffListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_stuff.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all_borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)


# Author view templates
class AuthorCreate(PermissionRequiredMixin ,CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


# Book view templates
class BookCreate(PermissionRequiredMixin ,CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')
