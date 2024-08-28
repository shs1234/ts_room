from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework.exceptions import ValidationError


class Room(models.Model):
    title = models.CharField(max_length=20, unique=True)
    current_participants = models.IntegerField(default=0)
    ready_participants = models.IntegerField(default=0)
    max_participants = models.IntegerField(choices=[(2, '2 players'), (4, '4 players')])
    players = models.JSONField(default=list)
    isPlaying = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title

    def user_in_room(self, username):
        return Room.objects.filter(players__contains=[username]).exists()

    def join(self, username):
        # 이미 현재 방에 속해 있을 경우, 아무것도 하지 않음
        if username in self.players:
            return
        # 다른 방에 이미 속해 있을 경우, 그 방에서 나가고 새로운 방에 참가
        if self.user_in_room(username):
            room = Room.objects.get(players__contains=[username])
            room.leave(username)
        self.players.append(username)
        self.current_participants = len(self.players)
        self.save()

    def leave(self, username):
        self.players.remove(username)
        self.current_participants = len(self.players)
        self.ready_reset()
        self.save()
        self.delete_empty_room()
    
    def ready_reset(self):
        self.ready_participants = 0
        self.save()
    
    def start(self):
        self.isPlaying = True
        self.save()
    
    def ready(self):
        self.ready_participants += 1
        self.save()

    def delete_empty_room(self):
        if self.current_participants == 0:
            self.delete()