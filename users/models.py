from django.contrib.auth.models import AbstractUser
from django.db import models
# from books.models import Author

# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default='default_profile.jpg')


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# class Followings(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     following =  models.ForeignKey(Author, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)