from . import views
from django.urls import path

urlpatterns = [
    path('store', views.store, name="store"),
    path('store/product/<str:pk>', views.storeProduct, name="store-product"),
    path('login/', views.loginPage, name="login"),
]