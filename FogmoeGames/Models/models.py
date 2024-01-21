from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
class games(models.Model):
    name = models.CharField(max_length=40)
    playerNum = models.IntegerField()
    
    def __str__(self):
        return f" {self.playerNum} 人 {self.name} "


# 定义一个表示聊天室的模型，包含房间名，房间密码，订阅者列表等字段
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    players = models.ManyToManyField(User, related_name="chatrooms", blank=True)##玩家

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
    

# 狼人杀
class WerewolfSaga(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    round = models.IntegerField(default=0)
    action = models.IntegerField(default=0)
    players = models.ManyToManyField(User, through='WerewolfSagaPlayer',blank=True)##玩家



    def __str__(self):
        return f"{self.name}"
    
class WerewolfSagaPlayer(models.Model):
    # 中间表模型
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    werewolfsaga = models.ForeignKey(WerewolfSaga, on_delete=models.CASCADE)
    playerstatus = models.IntegerField(default=0)
    playernumber = models.IntegerField(default=0)
    role = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.playernumber} : {self.player.username}"