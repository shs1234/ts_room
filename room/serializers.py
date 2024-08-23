from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['title', 'max_participants']

    def valid_max_participants(self, value):
        if value not in [2, 4]:
            raise serializers.ValidationError('max_participants should be 2 or 4')
        return value