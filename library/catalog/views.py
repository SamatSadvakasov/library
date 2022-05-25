from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


def index(request):
    # EXAMPLE
    # my_car = request.session.get('my_car', 'mini')
    # request.session['my_car'] = 'mini'
    # request.session.modified = True

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }
    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorDetailView(generic.DetailView):
    model = Author
