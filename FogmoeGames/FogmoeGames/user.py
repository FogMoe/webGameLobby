from django.shortcuts import redirect, render
import datetime
from django.contrib.auth.models import User #django自带的User模型
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_
from django.contrib.auth import logout
import re

def validate_user_input(username, password, email):
    # 用户名不允许包含特定的不常见符号（黑名单）
    if re.search(r'[<>{}[\]~`]', username):
        return False
    # 用户名长度不超过8位
    if len(username) > 8:
        return False
    if len(username) < 2:
        return False
    # 密码必须6位以上12位以下，可以包含字母、数字和符号
    if not re.match(r'^[A-Za-z0-9@#$%^&+=]{6,12}$', password):
        return False
    # 电子邮件格式校验
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    return True

def login(request):
    context          = {}
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request,username=username,password=password)

    if not user:
        context['message'] = '用户名或密码错误~' 
        return render(request, 'login.html', context) 
    
    user.last_login=datetime.datetime.now()
    context['message'] = '登录成功~' 
    context['user'] = user
    user.save()
    login_(request, user)
    return  redirect('index') #重定向到index

def register(request):
    context          = {}
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    

    if not validate_user_input(username,password,email):
        context['message'] = '输入错误，请检查~' 
        return render(request,'register.html', context) 
    
    if User.objects.filter(username=username).exists():
        context['message'] = '用户名已存在~' 
        return render(request,'register.html', context) 
    
    last_login = datetime.datetime.now()
    user=User.objects.create_user(username=username,password=password,email=email,last_login=last_login)
    context['message'] = '注册成功~' 
    context['user'] = user 
    login_(request, user)
    return  redirect('index') #重定向到index
    

def unLogin(request):
    context          = {}
    logout(request)
    context['message'] = '已退出登录' 
    return  redirect('index') #重定向到index
    #return HttpResponse("Hello world ! ")