from re import search
from django.db import models
from django.db.models import *
from django.utils import timezone
from django.contrib.auth.models import User, auth, Group
import datetime


class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=1000,null=True)
    lastname = models.CharField(max_length=1000,null=True,blank=True)
    email = models.CharField(max_length=100,null=True)
    profile_pic = models.ImageField(upload_to = 'profilepics',null=True,blank=True)
    Institute = models.CharField(max_length=1000,null=True)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "Register Table"


class Post(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post_title = models.CharField(max_length=200,null=True)
    desc = models.TextField(null=True)
    category = models.CharField(max_length=50)
    place = models.CharField(max_length=1000, null=True)
    cover = models.ImageField(upload_to='covers',null=True)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    comments = models.ManyToManyField(User,related_name='comments',blank=True)
    post_date = models.DateField(auto_now_add=True,null=True)
    sha = models.CharField(max_length=100,null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural = "News"
    def num_likes(self):
        return self.likes.count()

class PostImage(models.Model):
    cover = models.ImageField(upload_to='covers',null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)

class Comment(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    desc = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)