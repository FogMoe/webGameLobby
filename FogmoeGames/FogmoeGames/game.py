import threading,time
from django.shortcuts import render
from Models.models import games,ChatRoom
from django.core.exceptions import ObjectDoesNotExist

def dingshishanchuroom(room,shijian):
    # 创建一个线程，目标函数是 delayed_execution
    thread = threading.Thread(target=lambda: [time.sleep(shijian), deleteroom(room)])
    # 启动线程
    thread.start()

def deleteroom(room ):
    if not(room.subscribers.all().exists()):
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

    match gameId:
        case 1:##100人聊天室
            user=request.user
            chatRoom=ChatRoom(name=roomName,password=password) ##创建游戏模型
            chatRoom.save()
            context['roomId'] = chatRoom.id##获取房间id
            dingshishanchuroom(chatRoom,120)
            return render(request, 'joinroom.html', context)
            
        case 2:##狼人杀
            return render(request, 'index.html', context)
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
            try:
                chatRoom=ChatRoom.objects.get(id=roomId) ##获取游戏对象
            except ObjectDoesNotExist: ##如果没有根据id获取到对象，说明这个房间不存在
                context['message'] = '没有这个房间！'
                gameList = games.objects.all()
                context['gameList'] = gameList 
                return render(request, 'joinroom.html', context) 
            else:
                if chatRoom.password == password: 
                    print('aaaa')
                    try:##判断是不是已经在房间里了
                        chatRoom.subscribers.get(id=user.id)
                    except ObjectDoesNotExist:
                        return render(request, 'chatroom.html', context)
                    else:
                        context['message'] = '你已经在这个房间里了！'
                        gameList = games.objects.all()
                        context['gameList'] = gameList 
                        return render(request, 'joinroom.html', context) 
                    
                else:##密码错误时
                    context['message'] = '密码错误！'
                    gameList = games.objects.all()
                    context['gameList'] = gameList 
                    return render(request, 'joinroom.html', context) 
        case 2:##狼人杀
            return render(request, 'index.html', context)
        case _:
            print('没有这个游戏')
            return render(request, 'joinroom.html', context)

