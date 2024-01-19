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
from . import views,user,testdb,game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('toLogin/', views.toLogin),
    path('toRegister/', views.toRegister),
    path('toLobby/', views.toLobbby),
    path('toLobby/', views.toLobbby),
    path('toJoinroom/', views.toJoinroom),
    path('toCreateroom/', views.toCreateroom),
    path('login/', user.login),
    path('register/', user.register),
    path('unLogin/', user.unLogin),
    path('createroom/', game.createroom),
    path('joinroom/', game.joinroom),
    path('', views.index),
    path('index/', views.index),
    path('testdb/', testdb.testdb),
    #path("", views.hello, name="hello"),
]