from cv2 import CLAHE
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from books.forms import BookReviewForm
from books.models import Book, BookReview
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

# class BooksViews(ListView):
#     template_name = 'list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2

# class BookDetailView(DetailView):
#     template_name = 'detail.html'
#     pk_url_kwarg = 'id'
#     model = Book


class BooksViews(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q','')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size',4)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page',1)
        page_obj =  paginator.get_page(page_num)
        
        return render(request, 'list.html', {'page_obj': page_obj, 'search_query': search_query})

class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        review_form = BookReviewForm()
        return render(request, 'detail.html', {'book': book, 'review_form': review_form})

class AddReviewView(LoginRequiredMixin,View):
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        review_form = BookReviewForm(request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                comment=review_form.cleaned_data['comment'],
                stars_given=review_form.cleaned_data['stars_given']
            )

            return redirect(reverse('books:detail', kwargs={'pk': pk}))
        return render(request, 'detail.html', {'book': book, 'review_form': review_form})
    
    
class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.bookreview_set.get(pk=review_pk)
        review_form = BookReviewForm(instance=review)
    
        return render(request, 'edit_review.html', {'book': book, 'review_form': review_form, 'review': review})
    
    def post(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.bookreview_set.get(pk=review_pk)
        review_form = BookReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'pk': book_pk}))
        return render(request, 'edit_review.html', {'book': book, 'review_form': review_form, 'review': review})
    
class ConfirmReviewView(LoginRequiredMixin, View):
    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.bookreview_set.get(pk=review_pk)
        return render(request, 'confirm_delete.html', {'book': book, 'review': review})
    
class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_pk, review_pk):
        book = Book.objects.get(pk=book_pk)
        review = book.bookreview_set.get(pk=review_pk)
        review.delete()
        messages.success(request, 'Your review has been deleted')
        
        return redirect(reverse('books:detail', kwargs={'pk': book_pk}))