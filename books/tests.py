from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser
# Create your tests here.
class BookTest(TestCase):
    def test_no_books(self):
       response = self.client.get(reverse('books:list'))
       self.assertContains(response, 'No books found')
    def test_books_list(self):
        Book.objects.create(title='1', descrption='1',isbn='1')
        Book.objects.create(title='2', descrption='2',isbn='2')
        # Book.objects.create(title='3', descrption='3',isbn='3')
        
        response = self.client.get(reverse('books:list'))
        books = Book.objects.all()
        
        for book in books:
            self.assertContains(response, book.title)
    def test_detail_view(self):
        book = Book.objects.create(title='1', descrption='1',isbn='1')
        response = self.client.get(reverse('books:detail', args=[book.id]))
        self.assertContains(response, book.title)
        self.assertContains(response, book.descrption)
    def test_search_view(self):
        book1= Book.objects.create(title='toshkent', descrption='1',isbn='1')
        book2= Book.objects.create(title='the', descrption='2',isbn='2')
        book3= Book.objects.create(title='test01', descrption='3',isbn='3')
        
        response = self.client.get(reverse('books:list') + '?q=the')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)
        response = self.client.get(reverse('books:list') + '?q=tosh')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)
        response = self.client.get(reverse('books:list') + '?q=test01')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)
class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", descrption="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="testuser", first_name="testuser", last_name="testusers", email="jrahmonov2@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="testuser", password="somepass")

        self.client.post(reverse("books:reviews", kwargs={"pk": book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
    def test_invate_review(self):
        book = Book.objects.create(title="Book1", descrption="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="testuser", first_name="testuser", last_name="testusers", email="jrahmonov2@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="testuser", password="somepass")

        self.client.post(reverse("books:reviews", kwargs={"pk": book.id}), data={
            "stars_given": 6,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(),False)