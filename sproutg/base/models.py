from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Profile(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
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
    
    game_list = models.ManyToManyField(Game, related_name='game_list', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
  
    def __str__(self):
        return self.developer_name

  
class Review(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    stars = ('0', '1', '2', '3', '4', '5')
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
  
    def __str__(self):
        return self.name
    
    
class Transaction(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
  
    created = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.name
    
    
