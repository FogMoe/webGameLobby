"""
URL configuration for FogmoeGames project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import room, views,user

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('toLogin/', views.toLogin, name='toLogin'),
    path('toRegister/', views.toRegister, name='toRegister'),
    path('toLobby/', views.toLobbby, name='toLobby'),
    path('toLobby/', views.toLobbby, name='toLobby'),
    path('toJoinroom/', views.toJoinroom, name='toJoinroom'),
    path('toCreateroom/', views.toCreateroom, name='toCreateroom'),
    path('login/', user.login, name='login'),
    path('register/', user.register, name= 'register'),
    path('unLogin/', user.unLogin, name='unLogin'),
    path('createroom/', room.createroom, name='createroom'),
    path('joinroom/', room.joinroom, name='joinroom'),
    path('index/', views.index),
    path('', views.index,name='index'),
]