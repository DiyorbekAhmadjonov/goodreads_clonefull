from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user
# Create your tests here.


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'), 
            data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'CustomUser',
            'email': 'test@gmail.com',
            'password': 'testpassword',
        })
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'CustomUser')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password('testpassword'))
        
    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'), 
            data={
            'first_name': 'Test',
            'email': 'test@gmail.com'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'), 
            data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'CustomUser',
            'email': 'testpassword',
            'password': 'testpassword',
        })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
    def test_unique_username(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
            last_name='CustomUser',
            email='test@mail.com',
            password='testpassword',
        )
        response = self.client.post(
            reverse('users:register'),
            data={
            'username':'testuser',
            'first_name':'Test',
            'last_name':'CustomUser',
            'email':'test@mail.com',
            'password':'testpassword',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
            
class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
        )
        self.user.set_password('testpassword')
        self.user.save()
    
    def test_successful_login(self):
        respomns =  self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'testpassword',
            }
        )
        getuser = get_user(self.client)
        self.assertEqual(getuser.username, 'testuser')
    def test_wrong_credentials(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'testusesr',
                'password': 'wrongpassword',
            }
        )
        self.assertFalse(get_user(self.client).is_authenticated)
    def test_wrong_password(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'wrongpassword',
            }
        )
        self.assertFalse(get_user(self.client).is_authenticated)
        
class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(
            reverse('users:profile')
        )
        self.assertEqual(response.url,reverse('users:login') + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)
    def test_profile_details(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
        )
        user.set_password('testpassword')
        user.save()
        self.client.login(
            username='testuser',
            password='testpassword',
        )
        response = self.client.get(
            reverse('users:profile')
        )
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Test')
        self.assertEqual(response.status_code, 200)
    def test_logout(self):
        self.client.login(
            username='testuser',
            password='testpassword',
        )
        response = self.client.get(
            reverse('users:logout')
        )
        users =get_user(self.client)
        self.assertFalse(users.is_authenticated,False)
        self.assertEqual(response.status_code, 302)
    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
            email='asd@gmail.com'
        )
        user.set_password('testpassword')
        user.save()
        self.client.login(
            username='testuser',
            password='testpassword',
        )
        response = self.client.post(
            reverse('users:profile_edit'),
            data= {
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'CustomUser',
                'email': 'ddd@gmail.com'
            }
        )
        users= CustomUser.objects.get(pk=user.pk)
        self.assertEqual(users.username, 'testuser')
        self.assertEqual(users.first_name, 'Test')
        self.assertEqual(users.last_name, 'CustomUser')
        self.assertEqual(users.email, 'ddd@gmail.com')
        