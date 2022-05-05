from django.urls import path

from .views import BooksViews,BookDetailView,AddReviewView,EditReviewView,ConfirmReviewView,DeleteReviewView
app_name = 'books'
urlpatterns = [
    path('', BooksViews.as_view(), name='list'),
    path('<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:pk>/reviews/', AddReviewView.as_view(), name='reviews'),
    path('<int:book_pk>/reviews/<int:review_pk>/edit', EditReviewView.as_view(), name='edit_review'),
    path('<int:book_pk>/reviews/<int:review_pk>/delete/confirm', ConfirmReviewView.as_view(), name='confirm_delete_review'),
    path('<int:book_pk>/reviews/<int:review_pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]