from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name="store"),
    path('product/<str:pk>', views.storeProduct, name="store-product"),
    path('cart/', views.storeCart, name="cart"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
]