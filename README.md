# FogMoe-webGameLobby
待补充~

## 从环境搭建到启动服务端

[下载安裝python](https://www.python.org/downloads/release/python-3121/)

### 安裝库
```python
pip install Django==5.0.1 #django
pip install PyMySQL #数据库操作模块
pip install channels #websocket 以后换成 pip install channels-redis
pip install daphne
```

### 根据settings.py的DATABASES中的参数创建数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎
        'NAME': 'FogmoeGames', # 数据库名称
        'HOST': '127.0.0.1', # 数据库地址，本机 ip 地址 127.0.0.1 
        'PORT': 3306, # 端口 
        'USER': 'admin',  # 数据库用户名
        'PASSWORD': '123456', # 数据库密码
    }
}
```

### 更新数据库

```python
python manage.py makemigrations # 根据models.py生成
python manage.py migrate # 创建表结构
```

### 添加默认数据
[INSERT](http://localhost/phpMyAdmin4.8.5/url.php?url=https://dev.mysql.com/doc/refman/5.5/en/insert.html)
```sql
 INTO `models_games` (`id`, `name`, `playerNum`)
```
 [VALUES](http://localhost/phpMyAdmin4.8.5/url.php?url=https://dev.mysql.com/doc/refman/5.5/en/miscellaneous-functions.html#function_values)
```sql
 (NULL, '聊天室', '100'), (NULL, '狼人杀', '6')
```

### 修改settings.py中的hosts
```python
ALLOWED_HOSTS = ['127.0.0.1']
```

### 启动django
```python
python manage.py runserver 0.0.0.0:8001
```


