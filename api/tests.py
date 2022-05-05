from re import S
from rest_framework.reverse import reverse
from django.test import TestCase
from books.models import BookReview,Book
from users.models import CustomUser
from rest_framework.test import APITestCase
# Create your tests here.

class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='test_user',first_name='test',last_name='user')
        self.user.set_password('test_password')
        self.user.save()
        self.client.login(username='test_user',password='test_password')   
                              
     
    def test_book_review_detail(self):
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='1234')
        br = BookReview.objects.create(stars_given=5,comment='test_comment',book=book,user=self.user)
        response = self.client.get(reverse('api:review-detail', kwargs={'pk': br.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'test_comment')
        self.assertEqual(response.data['id'], br.pk)
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'],'test_book')
        self.assertEqual(response.data['book']['descrption'],'test_descrption')
        self.assertEqual(response.data['book']['isbn'],'1234')
        self.assertEqual(response.data['user']['id'], br.user.id)
        self.assertEqual(response.data['user']['username'],'test_user')
        self.assertEqual(response.data['user']['first_name'],'test')
        self.assertEqual(response.data['user']['last_name'],'user')
    
    def test_delete_review(self):
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='1234')
        br = BookReview.objects.create(stars_given=5,comment='test_comment',book=book,user=self.user)
        response = self.client.delete(reverse('api:review-detail', kwargs={'pk': br.pk}))
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(pk=br.pk).exists())
        
    def test_update_review(self):
        
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='1234')
        br = BookReview.objects.create(stars_given=5,comment='test_comment',book=book,user=self.user)
        response = self.client.patch(reverse('api:review-detail', kwargs={'pk': br.pk}),data={'stars_given':4,'comment':'test_comment_updated'})
        br.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        
    def test_put_review(self):
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='5')
        br = BookReview.objects.create(stars_given=5,comment='test_comment',book=book,user=self.user)
        response = self.client.put(reverse('api:review-detail', kwargs={'pk': br.pk}),
                                   data={'stars_given':4,'comment':'test_comment_updated','book_id':book.pk,'user_id':self.user.pk})
        br.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'test_comment_updated')
        
    

    
    
        
    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='test_user_two',first_name='test_two',last_name='user_two')
        user_two.set_password('test_password')
        user_two.save()
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='5')
        br = BookReview.objects.create(stars_given=5,comment='test_comment',book=book,user=self.user)
        br_two = BookReview.objects.create(stars_given=3,comment='test_comment1',book=book,user=user_two)
        response = self.client.get(reverse('api:review-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][1]['comment'], 'test_comment')
        self.assertEqual(response.data['results'][1]['id'], br.pk)
        self.assertEqual(response.data['results'][1]['book']['id'], br.book.id)
        self.assertEqual(response.data['results'][0]['stars_given'], 3)
        self.assertEqual(response.data['results'][0]['comment'], 'test_comment1')
        self.assertEqual(response.data['results'][0]['id'], br_two.pk)
        self.assertEqual(response.data['results'][0]['book']['id'], br_two.book.id)
        
    def test_create_review(self):
        book = Book.objects.create(title='test_book',descrption='test_descrption',isbn='5')
        response = self.client.post(reverse('api:review-list'),
                                    data={'stars_given':4,'comment':'test_comment','book_id':book.pk,'user_id':self.user.pk})
        
        br = BookReview.objects.get(book=book)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'test_comment')
        