from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
 
websocket_urlpatterns = [
    path('ws/chat/30/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:roomId>/', consumers.ChatConsumer.as_asgi()),
    path('ws/some_path/', consumers.YourConsumer.as_asgi()),
 ]

# 定义路由器
application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})