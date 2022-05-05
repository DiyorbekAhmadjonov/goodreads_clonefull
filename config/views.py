from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview
def index(request):
    return render(request, 'landing.html')

def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    page_num = request.GET.get('page_num', 1)
    paginator = Paginator(book_reviews, page_size)
    page_obj = paginator.get_page(page_num)
    return render(request, 'home.html', {'page_obj': page_obj})