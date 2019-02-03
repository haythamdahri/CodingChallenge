from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "challenge"


urlpatterns = [
    #--------------- Home view ---------------
    path('', views.HomeView.as_view(), name="home"),
    #--------------- Login view ---------------
    path('login/', views.LoginView.as_view(), name="login"),
    #--------------- Sign Up view ---------------
    path('registrer/', views.RegisterView.as_view(), name="registrer"),
    #--------------- Preferred shops view ---------------
    path('preferred-shops/', views.PreferredShopsView.as_view(), name="preferred_shops"),
    #--------------- Logout view ---------------
    path('logout/', views.LogOut.as_view(), name="logout"),
    #--------------- Like shop ---------------
    path('like-shop/', views.like_shop, name="like_shop"),
    #--------------- Dislike shop ---------------
    path('dislike-shop/', views.dislike_shop, name="dislike_shop"),
    #--------------- Remove shop ---------------
    path('remove-shop/', views.remove_shop, name="remove_shop"),
]
