from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect
from .models import Developer, Genre, Review, Game, Customer, Profile
from .forms import SignUpForm, ProfileForm, ReviewForm, GameForm
from .decorators import unauthenticated_user, allowed_users
from .addsFunctions import pageHeader

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

def userCreator(request, group_name='customer'):
    valid = False
    user = None
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            group = Group.objects.get(name=group_name)
            group.user_set.add(user)
            Profile.objects.create(user=user)
            if group_name == 'customer':
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
        return redirect('profile-edit')
    else:
        return render(request, template_name='base/register_page.html', context=context)

def registerDev(request):
    logoutUser(request)
    form = SignUpForm()
    group = 'developer'
    user, valid = userCreator(request, group)
    context = {'form': form, 'group': group}
    if valid:
        login(request, user)
        return redirect('profile-edit')
    else:
        return render(request, template_name='base/register_page.html', context=context)

def store(request):
    extraContext = pageHeader(request, 'home')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # games = Game.objects.filter(Q(name__icontains=q)|Q(genres__name__icontains=q))
    games = Game.objects.filter(verified=True)
    genres = Genre.objects.all()
    
    context = {'games': games, 
               'genres': genres, 
               'highlights': games[:10]} | extraContext
    
    return render(request=request, template_name='base/store.html', context=context)

def storeProduct(request, pk):
    extraContext = pageHeader(request, 'product')
    form = ReviewForm()
    game = Game.objects.get(id=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = extraContext['curUser'].profile
            review.game = game
            review.star_rating = request.POST.get('star_rating')
            review.save()

    genres = Genre.objects.all()
    reviews = Review.objects.filter(game=game)
    highlights = Game.objects.all()[:3]

    try:
        curReview = Review.objects.get(game=game, profile=request.user.profile)
    except Review.DoesNotExist:
        curReview = None
        
    context = {'game': game, 
               'genres': genres, 
               'highlights': highlights, 
               'reviews': reviews, 
               'form': form,
               'curReview': curReview} | extraContext
    
    return render(request=request, template_name='base/store-product.html', context=context)

@login_required(login_url='/login')
@allowed_users(['customer', 'admin'])
def deleteReview(request, productid, reviewid):
    review = Review.objects.get(id=reviewid)
    review.delete()
    
    return redirect('store-product', productid)

@login_required(login_url='/login')
@allowed_users(['customer'])
def storeCart(request):
    extraContext = pageHeader(request, 'cart')
    userCustomer = Customer.objects.get(user=request.user)
    cart = userCustomer.cart.all()
    total = userCustomer.getTotalPrice()
    
    context = {'cart': cart, 'total': total} | extraContext
    
    return render(request=request, template_name='base/cart.html', context=context)

def storeSearch(request):
    extraContext = pageHeader(request, 'search')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searchGames = Game.objects.filter(Q(name__icontains=q)|Q(genres__name__icontains=q))
    games = searchGames.filter(verified=True)
    genres = Genre.objects.all()
    
    context = {'games': games, 
               'genres': genres, 
               'highlights': games[:10],
               'searchQuerry': q} | extraContext
    
    return render(request=request, template_name='base/store-search.html', context=context)

@login_required(login_url='/login')
@allowed_users(['customer'])
def addToList(request, gameList, gameid):
    customer = Customer.objects.get(user=request.user)
    game = Game.objects.get(id=gameid)
    
    if gameList == 'cart':
        customer.cart.add(game)
    elif gameList == 'wishlist':
        customer.wishList.add(game)
    
    return redirect('store');

@login_required(login_url='/login')
@allowed_users(['customer'])
def removeFromList(request, gameList, gameid):
    customer = Customer.objects.get(user=request.user)
    game = Game.objects.get(id=gameid)
    
    if gameList == 'cart':
        customer.cart.remove(game)
    elif gameList == 'wishlist':
        customer.wishList.remove(game)

    return redirect(gameList)

@login_required(login_url='/login')
@allowed_users(['customer'])
def storeWishlist(request):
    extraContext = pageHeader(request, 'cart')
    customer = Customer.objects.get(user=request.user)
    wishlist = customer.wishList.all()
    
    context = {'wishlist': wishlist} | extraContext
    
    return render(request=request, template_name='base/wishlist.html', context=context)

def mygames(request):
    extraContext = pageHeader(request, 'my games')
    userCustomer = Customer.objects.get(user=request.user)
    games = userCustomer.myGames.all()
    
    context = {'games': games} | extraContext
    
    return render(request=request, template_name='base/mygames.html', context=context)

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
    extraContext = pageHeader(request, 'edit profile')
    profile = extraContext['curUser'].profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            profile = form.save()
            
            if 'developer' in extraContext['userGroups']:
                developer = Developer.objects.get(user=request.user)
                developer.developer_name = request.POST.get('developer_name')
                developer.save()
                return redirect('dashboard-dev')
            else:
                return redirect('profile', request.user.id)
        else:
            messages.error(request, 'An error has occured during registration')
    
    context = {'form': form} | extraContext
    
    return render(request=request, template_name='base/profile-edit.html', context=context)

@login_required(login_url='/login')
@allowed_users(['developer'])
def devDashboard(request):
    extraContext = pageHeader(request, 'dashboard')
    user = extraContext['curUser']
    profile = Profile.objects.get(user=user)
    games = Game.objects.filter (devUser=user)
    form = GameForm()
    genres = Genre.objects.all()
    
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid:
            newGame = form.save(commit=False)
            newGame.devUser = user
            inputGenres = request.POST.getlist('genres')
            newGame.save()
            for x in inputGenres:
                newGame.genres.add(x)
            
            return redirect(request.path_info)
        else:
            messages.error(request, 'An error has occured during upload')
    
    context = { 'form': form,
                'profile': profile, 
                'games': games,
                'genres': genres} | extraContext
    
    return render(request=request, template_name='base/dashboard-dev.html', context=context)

@login_required(login_url='/login')
@allowed_users(['developer'])
def deleteGame(request, gameid):
    review = Game.objects.get(id=gameid)
    review.delete()
    
    return redirect(request.path_info)

def about(request):
    extraContext = pageHeader(request, 'developer profile')
    genres = Genre.objects.all()
    
    context = {'genres': genres} | extraContext
    
    return render(request=request, template_name='base/about.html', context=context)

@login_required(login_url='/login')
@allowed_users(['customer'])
def buyGames(request):
    userCustomer = Customer.objects.get(user=request.user)
    cart = userCustomer.cart.all()
    userCustomer.myGames.add(*cart)
    userCustomer.cart.clear()
    
    return redirect('mygames')

@login_required(login_url='/login')
@allowed_users(['admin'])
def adminDashboard(request):
    extraContext = pageHeader(request, 'Admin Dashboard')
    submittedGames = Game.objects.filter(verified = False)
    context = {'submittedGames': submittedGames} | extraContext
    
    return render(request=request, template_name='base/dashboard-admin.html', context=context)

@login_required(login_url='/login')
@allowed_users(['admin'])
def jempol(request, gameid):
    game = Game.objects.get(id=gameid)
    game.verified = True
    game.save()
    
    return redirect('dashboard-admin')