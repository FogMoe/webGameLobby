from django.shortcuts import render
from Models.models import games
 
def index(request):
    context          = {}
    context['hello'] = 'Hello Index!' #对html中传递hello变量
    return render(request, 'index.html', context) #对html跳转到index
    #return HttpResponse("Hello world ! ")
def toLogin(request):
    context          = {}
    return render(request, 'login.html', context) 
def toRegister(request):
    context          = {}
    return render(request, 'register.html', context) 
def toLobbby(request):
    context          = {}
    return render(request, 'lobby.html', context) 
def toJoinroom(request):
    context          = {}
    gameList = games.objects.all()
    context['gameList'] = gameList 
    return render(request, 'joinroom.html', context) 
def toCreateroom(request):
    context          = {}
    gameList = games.objects.all()
    context['gameList'] = gameList 
    return render(request, 'createroom.html', context) 

