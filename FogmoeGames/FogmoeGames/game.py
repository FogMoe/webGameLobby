from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.contrib.auth.models import User #django自带的User模型
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_
from django.contrib.auth import logout
from Models.models import games,ChatMessage,ChatRoom
from django.shortcuts import redirect
import re

def createroom(request):
    context          = {}
    gameId = request.POST['game']
    roomName=games.objects.get(id=gameId).__str__()
    password = request.POST['password']
    user=request.user
    chatRoom=ChatRoom(name=roomName,password=password)

    chatRoom.save()
    chatRoom.subscribers.add(user)
    context['roomId'] = chatRoom.id
    context['roomName'] = roomName

    return render(request, 'chatroom.html', context)
def joinroom(request):
    context          = {}
    gameId = request.POST['game']
    roomName=games.objects.get(id=gameId).__str__()
    roomId=request.POST['roomId']
    password = request.POST['password']
    user=request.user
    chatRoom=ChatRoom.objects.get(id=roomId) 
    chatRoom.subscribers.add(user)
    context['roomId'] = roomId
    context['roomName'] = roomName
    return render(request, 'chatroom.html', context)