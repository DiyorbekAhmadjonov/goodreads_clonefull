from django.contrib import admin
from .models import Book, Author, BookReview,BookAuthor
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn','descrption')
    
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email','bio')
    
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('user', 'book')
    list_display = ('user', 'book','comment','stars_given')

class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')
    list_display = ('book', 'author')
    
admin.site.register(Book, BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(BookReview,ReviewAdmin)
admin.site.register(BookAuthor,BookAuthorAdmin)