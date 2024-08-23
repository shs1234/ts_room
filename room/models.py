from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework.serializers import ValidationError

class Room(models.Model):
    title = models.CharField(max_length=20, unique=True)
    current_participants = models.IntegerField(default=0)
    max_participants = models.IntegerField(choices=[(2, '2 players'), (4, '4 players')])
    players = models.JSONField(default=list)  # JSON 리스트로 유저 ID나 이름을 저장
    isPlaying = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title

    def add_player(self, username):
        if self.current_participants < self.max_participants:
            if username not in self.players:
                self.players.append(username)
                self.current_participants += 1
                self.save()
            else:
                raise ValidationError("User is already in the room.")
        else:
            raise ValidationError("The room is full.")

    def remove_player(self, username):
        if username in self.players:
            self.players.remove(username)
            self.current_participants -= 1
            self.save()
        else:
            raise ValidationError("User is not in the room.")

    def start_game(self):
        if self.current_participants == self.max_participants:
            self.isPlaying = True
            self.save()
        else:
            raise ValidationError("The room is not full.")