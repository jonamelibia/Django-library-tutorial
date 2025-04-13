from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

   # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 1 
    def get_context_data(self, **kwargs):
        # Llame primero a la implementación base para obtener un contexto.
        context = super(BookListView, self).get_context_data(**kwargs)
        # Obtenga el blog del id y agréguelo al contexto.
        context['some_data'] = 'Estos son solo algunos datos'
        return context

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 1 

    def get_context_data(self, **kwargs):
        # Llame primero a la implementación base para obtener un contexto.
        context = super(AuthorListView, self).get_context_data(**kwargs)
        
        # Agregar un diccionario con los libros de cada autor
        authors = context['object_list']  # Lista de autores en la página actual
        author_books = {author: author.book_set.all() for author in authors}
        
        # Agregar los libros al contexto
        context['author_books'] = author_books
        return context

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
