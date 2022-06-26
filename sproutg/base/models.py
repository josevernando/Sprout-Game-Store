from math import floor
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
    
    class Meta:
        ordering = ['name']
    
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
    
    class Meta:
        ordering = ['-updated', '-created']
  
    def __str__(self):
        return self.name
    
    def getRatings(self):
        ratings = [s.star_rating for s in Review.objects.filter(game=self)]
        
        return ratings
    
    def hasReviews(self):
        ratings = self.getRatings()
        
        return len(ratings)>0
        
    def overallStar(self):
        ratings = self.getRatings()
        starsum = 0
        
        for x in ratings:
            starsum += float(x)
        overall_rating = starsum/len(ratings)
        
        fullStars = floor(overall_rating)
        halfStar = (overall_rating % fullStars) >= 0.5
        fullStars = range(fullStars)
        
        return fullStars, halfStar
    
    def sales(self):
        salesCount = Transaction.objects.filter(game=self).count()
        return salesCount
    
class Customer(models.Model):
    cart = models.ManyToManyField(Game, related_name='cart', blank=True)
    myGames = models.ManyToManyField(Game, related_name='myGames', blank=True)
    wishList = models.ManyToManyField(Game, related_name='wishList', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.user.username + "'s Customer Model"
    
    def getTotalPrice(self):
        prices = [float(x.price) for x in self.cart.all()]
        total = sum(prices)
        
        return total
        
    
class Developer(models.Model):
    developer_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
  
    def __str__(self):
        return self.developer_name
  
class Review(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    star_choices = ((f'{x}', f'{x}')for x in range(1,6))
    star_rating = models.CharField(max_length=1,choices=star_choices,default=3)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-updated', '-created']
  
    def __str__(self):
        return f"{self.profile.user.username} | {self.star_rating} | {self.game.name}"
    
    def loopStars(self):
        return range(int(self.star_rating))

    
class Transaction(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
  
    created = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.name
    
    
