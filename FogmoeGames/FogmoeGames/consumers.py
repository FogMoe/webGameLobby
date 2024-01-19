import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
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

class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        print('websocket建立连接时执行方法')
        print(self.scope)
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.roomId = self.scope['url_route']['kwargs']['roomId']
        self.room_group_name = 'chat_%s' % self.roomId
 
        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print('websocket断开时执行方法')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        print("# 从websocket接收到消息时执行函数")
        text_data_json = json.loads(text_data)
        user=self.scope['user']
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

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'({datetime_str}) {message}'
        }))