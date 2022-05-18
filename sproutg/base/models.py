from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Developer(models.Model):
    name = models.CharField(max_length=200)
    # GameList =
    
    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    publisher = models.CharField(max_length=200)
    price = models.FloatField()
    verified = models.BooleanField()
    # reviews = 
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    gameid = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Transaksi(models.Model):
    name = models.CharField(max_length=200)
    customerid = models.ForeignKey(User, on_delete=models.CASCADE)
    # gameid =
    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # myGames = models.TextField()
    # wishList=
    # transaksi =