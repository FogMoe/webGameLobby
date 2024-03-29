from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
 
websocket_urlpatterns = [
    path('ws/chat/<str:roomId>/', consumers.ChatConsumer.as_asgi(),name='chat'),
    path('ws/werewolfsaga/<str:roomId>/', consumers.WerewolfSagaConsumer.as_asgi(), name='werewolfsaga'),
 ]

# 定义路由器
application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})