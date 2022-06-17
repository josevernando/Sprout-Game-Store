from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Profile(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    profile_pic = models.ImageField(null=True, default='default-avatar.jpg')
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    birth_date = models.DateField(null=True)
    
    def __str__(self):
        return self.user.username + ' | ' + self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(Genre, related_name='genres', blank=True)
    devUser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    publisher = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    verified = models.BooleanField(default=False)
  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    cart = models.ManyToManyField(Game, related_name='cart', blank=True)
    myGames = models.ManyToManyField(Game, related_name='myGames', blank=True)
    wishList = models.ManyToManyField(Game, related_name='wishList', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.user.username + "'s Customer Model"
    
    
class Developer(models.Model):
    developer_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
  
    def __str__(self):
        return self.developer_name


class Approval(models.Model):
    subject = models.CharField(max_length=150)
    message = models.CharField(max_length=150)
    approved = models.BooleanField(blank=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True)
  
  
class Review(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    star_choices = ((f"{x/2}",f"{x/2}")for x in range(11))
    star_rating = models.CharField(max_length=3,choices=star_choices,default=2.5)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
  
    def __str__(self):
        return self.title
    
    
class Transaction(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
  
    created = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.name
    
    
