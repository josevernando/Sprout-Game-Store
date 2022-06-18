from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect
from .models import Developer, Genre, Review, Game, Customer, Profile
from .forms import SignUpForm, ProfileForm, ReviewForm
from .decorators import unauthenticated_user, allowed_users
from .addsFunctions import overallStar, pageHeader

# Create your views here.
@unauthenticated_user
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
        
    return render(request, 'base/login_page.html')

def logoutUser(request):
    logout(request)
    return redirect('store')

def userCreator(request, group='customer'):
    valid = False
    user = None
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            if group == 'customer':
                Customer.objects.create(user=user)
            else:
                Developer.objects.create(user=user)
            valid = True
        else:
            messages.error(request, 'An error has occured during registration')
    return user, valid

@unauthenticated_user
def registerUser(request):
    form = SignUpForm()
    group = 'customer'
    user, valid = userCreator(request, group)
    context = {'form': form, 'group': group}
    if valid:
        login(request, user)
        return redirect('profile-edit', request.user.id)
    else:
        return render(request, template_name='base/register_page.html', context=context)

@unauthenticated_user
def registerDev(request):
    form = SignUpForm()
    group = 'developer'
    user, valid = userCreator(request, group)
    context = {'form': form, 'group': group}
    if valid:
        login(request, user)
        return redirect('profile-edit', request.user.id)
    else:
        return render(request, template_name='base/register_page.html', context=context)

def store(request):
    extraContext = pageHeader(request, 'home')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    games = Game.objects.filter(Q(name__icontains=q)|Q(genres__name__icontains=q))
    genres = Genre.objects.all()
    
    context = {'games': games, 
               'genres': genres, 
               'highlights': games[:10]} | extraContext
    
    return render(request=request, template_name='base/store.html', context=context)

def storeProduct(request, pk):
    extraContext = pageHeader(request, 'product')
    game = Game.objects.get(id=pk)
    genres = Genre.objects.all()
    reviews = Review.objects.filter(game=game) 
    highlights = Game.objects.all()[:3]
    stars = overallStar(game)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = extraContext['curUser'].profile
            review.game = game
            review.save()

    context = {'game': game, 
               'genres': genres, 
               'highlights': highlights, 
               'reviews': reviews, 
               'form': form,
               'stars': stars} | extraContext
    
    return render(request=request, template_name='base/store-product.html', context=context)

def storeCart(request):
    extraContext = pageHeader(request, 'cart')
    userCustomer = Customer.objects.get(user=request.user)
    cart = userCustomer.cart.all()    
    
    context = {'cart': cart} | extraContext
    
    return render(request=request, template_name='base/cart.html', context=context)

def storeSearch(request):
    extraContext = pageHeader(request, 'search')
    games = Game.objects.all()

    context = {'games': games} | extraContext
    return render(request=request, template_name='base/store-search.html', context=context)

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

    return redirect(gameList)

@login_required(login_url='/login')
def storeWishlist(request):
    extraContext = pageHeader(request, 'cart')
    customer = Customer.objects.get(user=request.user)
    wishlist = customer.wishList.all()
    
    context = {'wishlist': wishlist} | extraContext
    
    return render(request=request, template_name='base/wishlist.html', context=context)

def userProfile(request, userid):
    extraContext = pageHeader(request, 'user profile')
    user = User.objects.get(id=userid)
    customer = Customer.objects.get(user=user)
    games = customer.myGames.all()[:4]
    profile = Profile.objects.get(user=user)
    
    context = {'profile': profile, 
               'games': games} | extraContext
    
    return render(request=request, template_name='base/profile.html', context=context)

def devProfile(request, userid):
    extraContext = pageHeader(request, 'developer profile')
    user = User.objects.get(id=userid)
    games = Game.objects.filter (devUser=user)
    profile = Profile.objects.get(user=user)
    
    context = {'profile': profile, 
               'games': games} | extraContext
    
    return render(request=request, template_name='base/profile-dev.html', context=context)

@login_required(login_url='/login')
def userProfileEdit(request):
    Profile.objects.get_or_create(user=request.user)
    extraContext = pageHeader(request, 'edit profile')
    form = ProfileForm(instance=extraContext['curUser'].profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=extraContext['curUser'].profile)
        if form.is_valid:
            profile = form.save()
            
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'An error has occured during registration')
    
    context = {'form': form} | extraContext
    
    return render(request=request, template_name='base/profile-edit.html', context=context)

def about(request):
    extraContext = pageHeader(request, 'developer profile')
    genres = Genre.objects.all()
    
    context = {'genres': genres} | extraContext
    
    return render(request=request, template_name='base/about.html', context=context)