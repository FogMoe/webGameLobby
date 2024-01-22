import json
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
        if room.round == 0:
            if text_data_json['message'] == 'unready':
                player.playerstatus = 0
                player.save()

            if text_data_json['message'] == 'ready':
                player.playerstatus = 1
                player.save()
                ##每有人准备时 判断房间中所有人是否准备
                r=True
                for p in roomPlayer:
                    if p.playerstatus == 0:r=False
                if r:
                    room.round = 1
                    room.save()


        ##第一阶段初始化
        if room.round == 1:
            ##赋予编号
            i=0
            for p in roomPlayer:
                i+=1
                p.playernumber = i
                p.save()
            ##赋予角色
            if(WerewolfSagaPlayer.objects.filter(playernumber=1,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=1,werewolfsaga_id=self.roomId)
                p.role=1
                p.playerstatus = 2
                p.save()
            if(WerewolfSagaPlayer.objects.filter(playernumber=2,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=2,werewolfsaga_id=self.roomId)
                p.role=2
                p.playerstatus = 2
                p.save()
            if(WerewolfSagaPlayer.objects.filter(playernumber=3,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=3,werewolfsaga_id=self.roomId)
                p.role=3
                p.playerstatus = 2
                p.save()
            if(WerewolfSagaPlayer.objects.filter(playernumber=4,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=4,werewolfsaga_id=self.roomId)
                p.role=3
                p.playerstatus = 2
                p.save()
            if(WerewolfSagaPlayer.objects.filter(playernumber=5,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=5,werewolfsaga_id=self.roomId)
                p.role=3
                p.playerstatus = 2
                p.save()
            if(WerewolfSagaPlayer.objects.filter(playernumber=6,werewolfsaga_id=self.roomId).exists()):
                p=WerewolfSagaPlayer.objects.get(playernumber=6,werewolfsaga_id=self.roomId)
                p.role=1
                p.playerstatus = 2
                p.save()
            room.round = 2
            room.save()
            # 给玩家发送信息
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': '现在是晚上，请狼人和女巫鲨鱼人'
                }
            )

        ##第二阶段 游戏真正开始
        if room.round == 2:
            match text_data_json['message']:
                case 'killp1':
                    p=WerewolfSagaPlayer.objects.get(playernumber=1,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                case 'killp2':
                    p=WerewolfSagaPlayer.objects.get(playernumber=2,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                case 'killp3':
                    p=WerewolfSagaPlayer.objects.get(playernumber=3,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                case 'killp4':
                    p=WerewolfSagaPlayer.objects.get(playernumber=4,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                case 'killp5':
                    p=WerewolfSagaPlayer.objects.get(playernumber=5,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                case 'killp6':
                    p=WerewolfSagaPlayer.objects.get(playernumber=6,werewolfsaga_id=self.roomId)
                    p.playerstatus = 3
                    p.save()
                    
        # 发送消息到频道组，频道组调用chat_message方法
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
        onlinelist=''
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

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'onlinelist': f'{onlinelist}',
            'role': f'{str(role)}',
            'playernumber': f'{str(playernumber)}',
            'username': f'{str(username)}',
            'round': f'{str(round)}',
            'playerstatus': f'{str(playerstatus)}',
            'action': f'{str(action)}'
        }))


