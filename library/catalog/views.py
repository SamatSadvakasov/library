from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


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
        'num_auth ors': num_authors
    }
    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
     model = Book
     paginate_by = 1


      # context_object_name = 'book_list'
     # queryset = Book.objects.filter(title__icontains = 'Potter')[:5]
     # template_name = 'books/my_book.html'


class BookDetailView(generic.DetailView):
    model = Book


