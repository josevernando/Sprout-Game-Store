from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect
from .models import Review, Game, Customer, Profile
from .forms import SignUpForm, ProfileForm

# Create your views here.

def breadCrumbs(request):
    crumbs = (request.path).split('/')[1:-1]
    print(crumbs)
    return crumbs

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

def registerUser(request):
    form = SignUpForm()
    
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            customer = Customer.objects.create(user=user)
            login(request, user)
            return redirect('profile-edit', request.user.id)
        else:
            messages.error(request, 'An error has occured during registration')
  
    return render(request, 'base/register_page.html')

def store(request):
    page = 'home'
    crumbs = breadCrumbs(request)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    games = Game.objects.filter(name__icontains=q)
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'games': games, 'crumbs': crumbs, 'page': page}
    return render(request=request, template_name='base/store.html', context=context)

def storeProduct(request, pk):
    page = 'product'
    crumbs = breadCrumbs(request)
    game = Game.objects.get(id=pk)
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'game': game, 'crumbs': crumbs, 'page': page}
    return render(request=request, template_name='base/store-product.html', context=context,)

def storeCart(request):
    page = 'cart'
    crumbs = breadCrumbs(request)
    userCustomer = Customer.objects.get(user=request.user)
    cart = userCustomer.cart.all()    
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'cart': cart, 'crumbs': crumbs, 'page': page}
    return render(request=request, template_name='base/cart.html', context=context)

def storeSearch(request):
    page = 'Search'
    crumbs = breadCrumbs(request)
    games = Game.objects.all()
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'games': games, 'crumbs': crumbs, 'page': page}
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
    page = 'wishlist'
    crumbs = breadCrumbs(request)
    customer = Customer.objects.get(user=request.user)
    wishlist = customer.wishList.all()
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'wishlist': wishlist, 'crumbs': crumbs, 'page': page}
    
    return render(request=request, template_name='base/wishlist.html', context=context)

def userProfile(request, userid):
    page = 'profile'
    crumbs = breadCrumbs(request)
    user = User.objects.get(id=userid)
    customer = Customer.objects.get(user=user)
    games = customer.myGames.all()[:4]
    profile = Profile.objects.get(user=user)
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'profile': profile, 'games': games, 'crumbs': crumbs, 'page': page}
    return render(request=request, template_name='base/profile.html', context=context)

def userProfileEdit(request, userid):
    page = 'edit profile'
    crumbs = breadCrumbs(request)
    user = User.objects.get(id=userid)
    profile, created = Profile.objects.get_or_create(user=user)
    
    form = ProfileForm() if created else ProfileForm(instance=profile)
    if request.method == 'POST':
        if form.is_valid:
            profile.full_name = request.POST.get('full_name')
            profile.birth_date = request.POST.get('birth_date')
            profile.description = request.POST.get('description')
            profile.save()
            
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'An error has occured during registration')
    
    curProfile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = {'curProfile': curProfile, 'profile': profile,'form': form, 'crumbs': crumbs, 'page': page}
    return render(request=request, template_name='base/profile-edit.html', context=context)