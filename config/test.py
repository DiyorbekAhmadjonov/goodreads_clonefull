from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from books.models import Book, BookReview

class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", descrption="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="testuser", first_name="testuser", last_name="testusers", email="test@gmail.com",
        )
        user.set_password("somepass")
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Good!") 
        review2 =BookReview.objects.create(book=book, user=user, stars_given=1, comment="Nice book")
        review3 =BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good")
        response = self.client.get(reverse("home_page") + "?page_size=2")
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
        
        