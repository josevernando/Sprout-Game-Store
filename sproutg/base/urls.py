from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name="store"),
    path('product/<str:pk>', views.storeProduct, name="store-product"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('wishlist/', views.storeWishlist, name="wishlist"),
    path('cart/', views.storeCart, name="cart"),
    path('add/<str:gameList>/<str:gameid>', views.addToList, name="addToList"),
    path('remove/<str:gameList>/<str:gameid>', views.removeFromList, name="removeFromList"),
    
]