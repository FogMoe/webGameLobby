import json
import threading
import time
import asyncio
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from Models.models import ChatRoom,WerewolfSaga,WerewolfSagaPlayer

import datetime

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        response = {
            'message': data['message']
        }
        await self.send(text_data=json.dumps(response))

##------------------聊天室---------------------------
class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        print('websocket建立连接时执行方法')
        print(self.scope)
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.roomId = self.scope['url_route']['kwargs']['roomId']
        self.room_group_name = 'chat_%s' % self.roomId
 
        room=ChatRoom.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        room.players.add(user) ##房间添加玩家

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

        # 加入房间的消息
        message=str(user.username)+'加入了房间！'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # 同步玩家列表
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'onlinelist_message'
            }
        )

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print('websocket断开时执行方法')
        room=ChatRoom.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        room.players.remove(user) ##房间删除玩家
        ##房间无人时删除房间
        if not(room.players.all().exists()):
            print('这个房间没人了，删除房间')
            print(room)
            room.delete()

        # 退出房间的消息
        message=str(user.username)+'失踪了。┭┮﹏┭┮'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # 同步玩家列表
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'onlinelist_message'
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        print("# 从websocket接收到消息时执行函数")
        text_data_json = json.loads(text_data)
        room=ChatRoom.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        message = user.username+" : "+text_data_json['message']

        # 发送消息到频道组，频道组调用chat_message方法
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print( message)
        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'({datetime_str}) {message}'
        }))

    # 同步在线列表的方法
    def onlinelist_message(self, event):
        room=ChatRoom.objects.get(id=self.roomId)
        onlinelist=''
        for user in room.players.all():
            onlinelist += user.username + '\n'

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'onlinelist': f'{onlinelist}'
        }))




##------------------狼人杀---------------------------
class WerewolfSagaConsumer(WebsocketConsumer):
    wolfvote = [0,0,0,0,0,0]
    witchvote=[0,0,0,0,0,0]
    vote=[0,0,0,0,0,0]
    # websocket建立连接时执行方法
    def connect(self):
        print('websocket建立连接时执行方法')
        print(self.scope)
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.roomId = self.scope['url_route']['kwargs']['roomId']
        self.room_group_name = 'chat_%s' % self.roomId
 
        room=WerewolfSaga.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        room.players.add(user) ##房间添加玩家

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

        # 加入房间的消息
        message=str(user.username)+'加入了房间！'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # 同步玩家列表
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'info_message'
            }
        )

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print('websocket断开时执行方法')
        room=WerewolfSaga.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        room.players.remove(user) ##房间删除玩家
        ##房间无人时删除房间
        if not(room.players.all().exists()):
            print('这个房间没人了，删除房间')
            print(room)
            room.delete()

        # 退出房间的消息
        message=str(user.username)+'失踪了。┭┮﹏┭┮'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # 同步玩家列表
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'info_message'
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        print("# 从websocket接收到消息时执行函数")
        text_data_json = json.loads(text_data)
        room=WerewolfSaga.objects.get(id=self.roomId)##获取房间对象
        user=self.scope['user']##获取用户对象
        player=WerewolfSagaPlayer.objects.get(player__id=user.id,werewolfsaga_id=self.roomId)
        roomUsers=room.players.all()
        roomPlayer=WerewolfSagaPlayer.objects.filter(werewolfsaga_id=self.roomId)
        message = user.username+" : "+text_data_json['message']
        print(message)
        ##回合0
        if room.round==0 :
            if text_data_json['message'] == 'unready':
               WerewolfSagaPlayer.objects.filter(id=player.id).update(playerstatus=0)

            if text_data_json['message'] == 'ready':
                WerewolfSagaPlayer.objects.filter(id=player.id).update(playerstatus=1)
                ##每有人准备时 判断房间中所有人是否准备
                r=True
                for p in roomPlayer:
                    if p.playerstatus == 0:r=False
                if r:
                    room.round = 1
                    room.save()
                        


        ##第一阶段初始化
        if  room.round== 1:
            ##赋予编号
            i=0
            for p in roomPlayer:
                i+=1
                WerewolfSagaPlayer.objects.filter(id=p.id).update(playernumber=i)

            ##赋予角色
            if(WerewolfSagaPlayer.objects.filter(playernumber=1,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=1,werewolfsaga_id=self.roomId).update(role=1)
            if(WerewolfSagaPlayer.objects.filter(playernumber=2,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=2,werewolfsaga_id=self.roomId).update(role=2)
            if(WerewolfSagaPlayer.objects.filter(playernumber=3,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=3,werewolfsaga_id=self.roomId).update(role=3)
            if(WerewolfSagaPlayer.objects.filter(playernumber=4,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=4,werewolfsaga_id=self.roomId).update(role=3)
            if(WerewolfSagaPlayer.objects.filter(playernumber=5,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=5,werewolfsaga_id=self.roomId).update(role=3)
            if(WerewolfSagaPlayer.objects.filter(playernumber=6,werewolfsaga_id=self.roomId).exists()):
                WerewolfSagaPlayer.objects.filter(playernumber=6,werewolfsaga_id=self.roomId).update(role=1)
            #让所有玩家活着，并可以行动
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room).update(playerstatus=2)
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,role=1).update(action=1)
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,role=2).update(action=1)
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': '现在是晚上，请狼人和女巫鲨鱼人，60秒后夜晚结束。'
                }
            )
            WerewolfSaga.objects.filter(id=room.id).update(round=2)
            ##进入round2 60秒后变成round3
            
            threading.Thread(target=lambda: [time.sleep(15), WerewolfSaga.objects.filter(id=room.id).update(round=3),self.receive(text_data)]).start()

        ##第二阶段 游戏真正开始
        if  room.round== 2:
            match text_data_json['message']:
                case 'killp1':
                    print('这里进行投票计数1')
                    if player.role == 1:
                        self.wolfvote[0]+=1
                        print('这里进行投票计数2',self.wolfvote)
                    if player.role == 2:
                        self.witchvote[0]+=1
                        print('这里进行投票计数3',self.witchvote)
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp2':
                    if player.role == 1:
                        self.wolfvote[1]+=1
                    if player.role == 2:
                        self.witchvote[1]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp3':
                    if player.role == 1:
                        self.wolfvote[2]+=1
                    if player.role == 2:
                        self.witchvote[2]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp4':
                    if player.role == 1:
                        self.wolfvote[3]+=1
                    if player.role == 2:
                        self.witchvote[3]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp5':
                    if player.role == 1:
                        self.wolfvote[4]+=1
                    if player.role == 2:
                        self.witchvote[4]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp6':
                    if player.role == 1:
                        self.wolfvote[5]+=1
                    if player.role == 2:
                        self.witchvote[5]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人



        #夜晚结算
        if  room.round== 3:
            print('夜晚结算中')
            ##鲨了狼人和女巫投票的玩家
            max_wolfvote = self.wolfvote.index(max(self.wolfvote))
            max_witchvote = self.witchvote.index(max(self.witchvote))
            print('狼人投票数据：',self.wolfvote)
            print('狼人最大下标',max_wolfvote)
            print('女巫投票数据：',self.witchvote)
            print('女巫最大下标',max_witchvote)
            message='白天到了， 现在可以自由发言，60秒后白天结束。'
            if max(self.wolfvote)!=0:
                WerewolfSagaPlayer.objects.filter(playernumber=max_wolfvote+1,werewolfsaga_id=self.roomId).update(playerstatus = 3)
                message=f'狼鲨了{max_wolfvote+1}号玩家。\n'+message
            if max(self.witchvote)!=0:
                message=f'女巫鲨了{max_witchvote+1}号玩家。\n'+message
                WerewolfSagaPlayer.objects.filter(playernumber=max_witchvote+1,werewolfsaga_id=self.roomId).update(playerstatus = 3)

            # 给玩家发送信息
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{message}'
                }
            )
            #所有活着的人能动
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,playerstatus=2).update(action=1)
            #死了的请装死别动
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,playerstatus=3).update(action=0)
            #进入round4白天，60秒后进入夜晚
            WerewolfSaga.objects.filter(id=room.id,).update(round=4)
            threading.Thread(target=lambda: [time.sleep(15), WerewolfSaga.objects.filter(id=room.id).update(round=5),self.receive(text_data)]).start()

            ##白天
        if  room.round== 4 :
            # 发送消息到频道组，频道组调用chat_message方法
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
            match text_data_json['message']:
                case 'killp1':
                    self.vote[0]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp2':
                    self.vote[1]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp3':
                    self.vote[2]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp4':
                    self.vote[3]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp5':
                    self.vote[4]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人
                case 'killp6':
                    self.vote[5]+=1
                    WerewolfSagaPlayer.objects.filter(id=player.id).update(action=0)#杀死一个人后让用户不能再次杀人


            ##白天结算，进入夜晚
        if  room.round== 5 :
            print('投票数据：',self.vote)
            max_vote = self.vote.index(max(self.vote))
            if max(self.vote)!=0:
                WerewolfSagaPlayer.objects.filter(playernumber=max_vote+1,werewolfsaga_id=self.roomId).update(playerstatus = 3)
                role='角色'
                match WerewolfSagaPlayer.objects.get(playernumber=max_vote+1,werewolfsaga_id=self.roomId).role:
                    case 0:
                        role='鹿人'
                    case 1:
                        role='狼人'
                    case 2:
                        role='女巫'
                    case 3:
                        role='村民'
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f' {max_vote+1}号玩家被大家鲨了，死者是一个{role}。\n夜晚降临，还活着的狼人女巫可以继续吃小孩，60秒后夜晚结束。'
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f'白天过去了然而无事发生。\n夜晚降临，还活着的狼人女巫可以继续吃小孩，60秒后夜晚结束。'
                    }
                )

            
            #狼和女巫能动
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,role=1,playerstatus=2).update(action=1)
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,role=2,playerstatus=2).update(action=1)
            #死了的别动
            WerewolfSagaPlayer.objects.filter(werewolfsaga=room,playerstatus=3).update(action=0)
            WerewolfSaga.objects.filter(id=room.id).update(round=2)
            #进入round3
            threading.Thread(target=lambda: [time.sleep(15), WerewolfSaga.objects.filter(id=room.id).update(round=3),self.receive(text_data)]).start()
                




        # 同步玩家列表
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'info_message'
            }
        )

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'({datetime_str}) {message}'
        }))

    # 同步在线列表的方法
    def info_message(self, event):
        room=WerewolfSaga.objects.get(id=self.roomId)
        user=self.scope['user']
        player=WerewolfSagaPlayer.objects.get(player__id=user.id,werewolfsaga_id=self.roomId)
        playerstatus=player.playerstatus
        role=player.role
        playernumber=player.playernumber
        username=user.username
        round=room.round
        action=room.action
        playeraction=player.action
        onlinelist=''
        lifelist=''
        for u in room.players.all():
            player=WerewolfSagaPlayer.objects.get(player__id=u.id,werewolfsaga_id=self.roomId)
            ps='状态'
            match player.playerstatus:
                case 0:
                    ps='未准备'
                case 1:
                    ps='准备'
                case 2:
                    ps='没死'
                case 3:
                    ps='死了'
            role='角色'
            match player.role:
                case 0:
                    role='鹿人'
                case 1:
                    role='狼人'
                case 2:
                    role='女巫'
                case 3:
                    role='村民'
            onlinelist += str(player.playernumber) +'. '+ u.username +' ('+ps+') '+role+  '\n'
            if player.playerstatus==2:lifelist +=str(player.playernumber) +','
        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'onlinelist': f'{onlinelist}',
            'role': f'{str(role)}',
            'playernumber': f'{str(playernumber)}',
            'username': f'{str(username)}',
            'round': f'{str(round)}',
            'playerstatus': f'{str(playerstatus)}',
            'action': f'{str(action)}',
            'playeraction': f'{str(playeraction)}',
            'lifelist': f'{str(lifelist)}'
        }))
    
