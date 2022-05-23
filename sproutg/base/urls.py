from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name="store"),
    path('login/', views.loginPage, name="login"),
]