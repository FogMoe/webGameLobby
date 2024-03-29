import threading,time
from django.shortcuts import redirect, render
from Models.models import games,ChatRoom,WerewolfSaga,WerewolfSagaPlayer

def dingshishanchuroom(room,shijian):
    # 创建一个线程，目标函数是 delayed_execution
    thread = threading.Thread(target=lambda: [time.sleep(shijian), deleteroom(room)])
    # 启动线程
    thread.start()

##如果房间没人，则删除房间
def deleteroom(room ):
    if not(room.players.all().exists()):
        print('这个房间没人了，删除房间')
        print(room)
        room.delete()
        print('这个房间没人加入，不如我们鲨了它吧')

def createroom(request):
    context          = {}
    gameId = int(request.POST['game'])##获取游戏id
    password = request.POST['password']
    roomName=games.objects.get(id=gameId).__str__()
    context['roomName'] = roomName
    context['gameId'] = gameId
    gameList = games.objects.all()
    context['gameList'] = gameList
    context['password'] = password

    match gameId:
        case 1:
            ##---------------聊天室--------------
            room=ChatRoom(name=roomName,password=password) ##创建游戏模型
            room.save()
            context['roomId'] = room.id##获取房间id
            dingshishanchuroom(room,60)##创建房间120s后没人的话就删除房间
            return render(request, 'joinroom.html', context)
            
        case 2:
            ##---------------狼人杀--------------
            room=WerewolfSaga(name=roomName,password=password) ##创建游戏模型
            room.save()
            context['roomId'] = room.id##获取房间id
            dingshishanchuroom(room,60)##创建房间120s后没人的话就删除房间
            return render(request, 'joinroom.html', context)
        case _:
            return render(request, 'createroom.html', context)


def joinroom(request):
    context          = {}
    gameId = int(request.POST['game'])
    roomName=games.objects.get(id=gameId).__str__()
    roomId=request.POST['roomId']
    password = request.POST['password']
    user=request.user
    context['roomId'] = roomId
    context['roomName'] = roomName
    print(roomId)
    print("阿斯蒂芬更健康了")
    if roomId=='':##如果房间号空着
        context['message'] = '房间号不要空着啊啊'
        gameList = games.objects.all()
        context['gameList'] = gameList 
        return render(request, 'joinroom.html', context) 
    match gameId:
        case 1:
            ##---------------聊天室--------------
            if not ChatRoom.objects.filter(id=roomId).exists():##如果房间不存在
                context['message'] = '没有这个房间！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
            
            room=ChatRoom.objects.get(id=roomId)
            if not room.password == password: 
                context['message'] = '密码错误！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
            
            if ChatRoom.objects.filter(id=roomId,players__id=user.id).exists():
                context['message'] = '你已经在这个房间里了！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
         
            return render(request, 'chatroom.html', context)
            

        case 2:
            ##---------------狼人杀--------------
            if not WerewolfSaga.objects.filter(id=roomId).exists():##如果房间不存在
                context['message'] = '没有这个房间！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
            
            room=WerewolfSaga.objects.get(id=roomId)
            if not room.password == password: 
                context['message'] = '密码错误！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
            
            if WerewolfSaga.objects.filter(id=roomId,players__id=user.id).exists():
                context['message'] = '你已经在这个房间里了！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
         
            return render(request, 'werewolfsaga.html', context)
        case _:
            print('没有这个游戏')
            return render(request, 'joinroom.html', context)

