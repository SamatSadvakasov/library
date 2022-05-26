import datetime
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm


@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


# @permission_required('catalog.can_mark_returned')
# # @permission_required('catalog.staff_member_required')
@login_required
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


class BookListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    paginate_by = 10


class AuthorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    paginate_by = 10


class BookDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'catalog.can_mark_returned'
    model = Book


class AuthorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'catalog.can_mark_returned'
    model = Author


class LoanedBooksByUserListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')


class LoanedBorrowerBookListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.staff_member_required'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='r').order_by('due_back')
