from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name="store"),
    path('product/<str:pk>/', views.storeProduct, name="store-product"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('wishlist/', views.storeWishlist, name="wishlist"),
    path('cart/', views.storeCart, name="cart"),
    path('add/<str:gameList>/<str:gameid>', views.addToList, name="addToList"),
    path('remove/<str:gameList>/<str:gameid>', views.removeFromList, name="removeFromList"),
    path('search', views.storeSearch, name="search"),
    path('profile/<str:userid>', views.userProfile, name="profile"),
    path('profile/edit/', views.userProfileEdit, name="profile-edit"),
    path('mygames/', views.mygames, name="mygames"),
    path('about/', views.about, name="about"),
    path('product/<str:productid>/delete-review/<str:reviewid>', views.deleteReview, name="delete-review"),
    path('register/dev/', views.registerDev, name="register-dev"),
    path('profile/dev/<str:userid>/', views.devProfile, name="profile-dev"),
    path('dashboard/', views.devDashboard, name="dashboard-dev"),
    path('dashboard/delete-game/<str:gameid>', views.deleteGame, name="delete-game"),
    
]
