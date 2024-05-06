from django.contrib import admin

# Register your models here.

from .models import Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'isbn', 'pages', 'created_at', 'updated_at')

admin.site.register(Book, BookAdmin)
