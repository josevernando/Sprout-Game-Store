from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Review, Game, Customer

# Create your views here.
def loginUser(request):
    
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
            return redirect ('store')
        
    context = {}
    return render(request, 'base/login_page.html', context)

def logoutUser(request):
    logout(request)
    return redirect('store')

def registerUser(request):
    form = UserCreationForm()
    context = {'form': form}
    
    if (request.method == 'POST'):
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'An error has occured during registration')
  
    return render(request, 'base/register_page.html', context)

def store(request):
    games = Game.objects.all()
    context = {'games': games}

    return render(request=request, template_name='base/store.html', context=context)

def storeProduct(request, pk):
    game = Game.objects.get(id=pk)
    context = {'game': game}
    return render(request=request, template_name='base/store-product.html', context=context)

def storeCart(request):
    userCustomer = Customer.objects.get(user=request.user)
    cart = userCustomer.cart.all()
    context = {'cart': cart}
    
    return render(request=request, template_name='base/cart.html', context=context)

@login_required(login_url='/login')
def addToList(request, gameList, gameid):
    
    customer = Customer.objects.get(user=request.user)
    game = Game.objects.get(id=gameid)
    if gameList == 'cart':
        customer.cart.add(game)
    elif gameList == 'wishlist':
        customer.wishList.add(game)
    
    return redirect(gameList);

@login_required(login_url='/login')
def removeFromList(request, gameList, gameid):
    customer = Customer.objects.get(user=request.user)
    game = Game.objects.get(id=gameid)
    if gameList == 'cart':
        customer.cart.remove(game)
    elif gameList == 'wishlist':
        customer.wishList.remove(game)
    
    return redirect(gameList);

def storeWishlist(request):
    customer = Customer.objects.get(user=request.user)
    wishlist = customer.wishList.all()
    context = {'wishlist': wishlist}
    
    return render(request=request, template_name='base/wishlist.html', context=context)