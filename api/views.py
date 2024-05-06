from django.http import HttpResponse
from django.shortcuts import render

from api.models import Book
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils import timezone
from faker import Faker
from django.db import connection

# Create your views here.

# @cache_page(timeout=60 * 30)  # cache for 30 minutes
# def home_cached(request):
#     # Check if cached data exists
#     cached_data = cache.get('cached_books')
    
#     if cached_data:
#         context = {}
#         context_list = []
#         for i in cached_data:
#             context_dict = {}
#             context_dict["title"] = i.title
#             context_dict["author"] = i.author
#             context_list.append(context_dict)
#         context["books"] = context_list
#         return render(request, "home.html", context)


# @cache_page(timeout=60 * 30)  # cache for 30 minutes
def home_cached(request):
    # Check if cached data exists
    # timer start
    import time
    start = time.time()

    cached_data = cache.get('cached_books')


    
    if cached_data:
        context = {'books': cached_data}
        end = time.time()
        print("Time taken to fetch cached books: ", end - start)

        return render(request, "home.html", context)
    else:
        return HttpResponse("Cached data not found.")




# def home_cached(request):
#     # Display the title with the highest rating in the home page
#     books = Book.objects.all()
#     context = {}
#     context_list = []
#     for i in books:
#         context_dict = {}
#         context_dict["title"] = i.title
#         context_dict["author"] = i.author
#         context_list.append(context_dict)
#     context["books"] = context_list
#     return render(request, "home.html", context)

def cache_books(request):
    # Fetch all books from the database
    books = Book.objects.all()
    
    # Convert book data to a format suitable for caching

    #timer start
    import time
    start = time.time()
    cached_books = [{'title': book.title, 'author': book.author} for book in books]
    
    # Cache the data
    cache.set('cached_books', cached_books, timeout=60 * 30)  # Cache for 30 minutes

    #timer end
    end = time.time()
    print("Time taken to cache books: ", end - start)
    
    if cache.get('cached_books'):
        return HttpResponse("Books cached successfully.")
    else:
        return HttpResponse("Failed to cache books.")


def home_cacheless(request):
    # Display the title with the highest rating in the home page
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT title, author FROM api_book")
    #     books = cursor.fetchall()
    books = Book.objects.all()
    context = {}
    context_list = []
    for i in books:
        context_dict = {}
        context_dict["title"] = i.title
        context_dict["author"] = i.author
        context_list.append(context_dict)
    context["books"] = context_list
    return render(request, "home.html",context)



def generate_fake_books(request):
    fake = Faker()

    # Generate and save 100,000 fake Book objects
    for _ in range(100000):
        title = fake.sentence(nb_words=5)
        author = fake.name()
        publication_date = fake.date_between(start_date='-50y', end_date='today')
        isbn = fake.isbn13()
        pages = fake.random_int(min=50, max=1000)
        created_at = timezone.now()
        updated_at = created_at

        Book.objects.create(
            title=title,
            author=author,
            publication_date=publication_date,
            isbn=isbn,
            pages=pages,
            created_at=created_at,
            updated_at=updated_at
        )

    return HttpResponse("100,000 fake books generated and saved successfully.")
