from django.shortcuts import render
from django.views import generic
import datetime
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.forms import RenewBookModelForm


@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

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


class BookListView(LoginRequiredMixin, generic.ListView):
     model = Book
     paginate_by = 5


      # context_object_name = 'book_list'
     # queryset = Book.objects.filter(title__icontains = 'Potter')[:5]
     # template_name = 'books/my_book.html'


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView( LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')


class LoanedBookListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.staff_member_required'
    model = BookInstance
    template_name = 'catalog/bookinstance_allborrowed.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='r').order_by('due_back')


class AuthorCreate(CreateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'catalog.staff_member_required'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']  # '__all__'
    initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):

    permission_required = 'catalog.staff_member_required'
    model = Author
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class AuthorDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'catalog.staff_member_required'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView ):
    permission_required = 'catalog.staff_member_required'
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'catalog.staff_member_required'
    model = Book
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class BookDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
    permission_required = 'catalog.staff_member_required'
    model = Book
    success_url = reverse_lazy('books')








