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