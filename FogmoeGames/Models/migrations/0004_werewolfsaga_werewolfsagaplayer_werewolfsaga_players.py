# Generated by Django 5.0.1 on 2024-01-21 07:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_chatroom_chatmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WerewolfSaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WerewolfSagaPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerstatus', models.IntegerField(default=0)),
                ('playernumber', models.IntegerField(default=0)),
                ('role', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('werewolfsaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.werewolfsaga')),
            ],
        ),
        migrations.AddField(
            model_name='werewolfsaga',
            name='players',
            field=models.ManyToManyField(blank=True, through='Models.WerewolfSagaPlayer', to=settings.AUTH_USER_MODEL),
        ),
    ]
