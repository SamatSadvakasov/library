from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@permission_required('catalog.can_mark_returned')
@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }
    return render(request, 'catalog/index.html', context=context)


class BookListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
     model = Book
     paginate_by = 1
     permission_required = 'catalog.can_mark_returned'


      # context_object_name = 'book_list'
     # queryset = Book.objects.filter(title__icontains = 'Potter')[:5]
     # template_name = 'books/my_book.html'


class BookDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Book
    permission_required = 'catalog.can_mark_returned'


class AuthorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 1
    permission_required = 'catalog.can_mark_returned'


class AuthorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Author
    permission_required = 'catalog.can_mark_returned'


class LoanedBooksByUserListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')







