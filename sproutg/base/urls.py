from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
]