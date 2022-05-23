from itertools import product
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Review, Game

# Create your views here.
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('home')
        
    context = {}
    return render(request, 'base/login_register.html', context)

def store(request):
    games = Game.objects.all()
    context = {'games': games}

    return render(request=request, template_name='base/store.html', context=context)

def storeProduct(request, pk):
    game = Game.objects.get(id=pk)
    context = {'game': game}
    return render(request=request, template_name='base/store-product.html', context=context)