import json
from channels.generic.websocket import AsyncWebsocketConsumer
from room.models import Room
from room.serializers import RoomSerializer
from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # 방 그룹에 참여하기
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.action_join(self.room_name, self.scope["user"].username)
        room_data = await self.get_room_data(self.room_name)
        message = {
            "action": "join",
            "text": f"{self.scope['user'].username} has joined the room.",
            "room_data": room_data,
        }
        # 방 그룹에 연결 메시지와 함께 방 데이터 보내기
        if room_data:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": json.dumps(message),
            })
        await self.accept()

    async def disconnect(self, close_code):
        await self.action_leave(self.room_name, self.scope["user"].username)
        room_data = await self.get_room_data(self.room_name)
        message = {
            "action": "leave",
            "text": f"{self.scope['user'].username} has left the room.",
            "room_data": room_data,
        }
        # 방 그룹에 연결 해제 메시지와 함께 방 데이터 보내기
        if room_data:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": json.dumps(message),
            })

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # WebSocket으로부터 메시지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        action = text_data_json["action"]
        if action == "message":
            message = text_data_json["message"]

            # 방 그룹에 메시지 보내기
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

        elif action == "start":
            await self.action_start(self.room_name)
            room_data = await self.get_room_data(self.room_name)
            text = f"{self.scope['user'].username} has started the game."
        elif action == "ready":
            await self.action_ready(self.room_name)
            room_data = await self.get_room_data(self.room_name)
            text = f"{self.scope['user'].username} is ready."
        message = {
            "action": action,
            "text": text,
            "room_data": room_data,
        }
        if room_data:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": json.dumps(message),
            })

    # 방 그룹으로부터 메시지 받기
    async def chat_message(self, event):
        message = event["message"]

        # WebSocket으로 메시지 보내기
        await self.send(text_data=json.dumps({"message": message}))
        # await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_room_data(self, room_name):
        try:
            room = Room.objects.select_related().get(pk=room_name)
            serializer = RoomSerializer(room)
            return serializer.data
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def action_join(self, room_name, username):
        try:
            room = Room.objects.get(pk=room_name)
            room.add_player(username)
        except ValidationError as e:
            return e.detail
    
    @database_sync_to_async
    def action_leave(self, room_name, username):
        try:
            room = Room.objects.get(pk=room_name)
            room.remove_player(username)
            room.ready_reset()
        except ValidationError as e:
            return e.detail

    @database_sync_to_async
    def action_start(self, room_name):
        try:
            room = Room.objects.get(pk=room_name)
            room.start_game()
        except ValidationError as e:
            return e.detail

    @database_sync_to_async
    def action_ready(self, room_name):
        try:
            room = Room.objects.get(pk=room_name)
            room.get_ready()
        except ValidationError as e:
            return e.detail

    @database_sync_to_async
    def action_ready_reset(self, room_name):
        try:
            room = Room.objects.get(pk=room_name)
            room.ready_reset()
        except ValidationError as e:
            return e.detail
