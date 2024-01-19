from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)
class games(models.Model):
    name = models.CharField(max_length=40)
    playerNum = models.IntegerField()
    
    def __str__(self):
        return f" {self.playerNum} 人 {self.name} "


# 定义一个表示聊天室的模型，包含房间名，房间密码，订阅者列表等字段
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name="chatrooms", blank=True)

    def __str__(self):
        return f"{self.name}"

# 定义一个表示聊天记录的模型，包含发送者，消息内容，发送时间等字段
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} : {self.content}"