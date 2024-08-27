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

        # 방 존재 여부 확인
        room_data = await self.get_room_data(self.room_name)
        if room_data == None :
            await self.send(text_data=json.dumps({"message": "Room does not exist."}))
            await self.close()

        # 방 그룹에 연결
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 방 참가(DB 업데이트)
        await self.action_join(self.room_name, self.scope["user"].username)

        # 방 참가 메시지 전송
        message = {
            "action": "join",
            "text": f"{self.scope['user'].username} has joined the room.",
            "room_data": room_data,
        }
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat.message",
            "message": json.dumps(message),
        })

        # WebSocket 연결 수락
        await self.accept()

    async def disconnect(self, close_code):
        # 방 그룹에서 나가기(DB 업데이트)
        await self.action_leave(self.room_name, self.scope["user"].username)

        # 방 나가기 메시지 전송
        room_data = await self.get_room_data(self.room_name)
        message = {
            "action": "leave",
            "text": f"{self.scope['user'].username} has left the room.",
            "room_data": room_data,
        }
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat.message",
            "message": json.dumps(message),
        })

        # 방 그룹에서 연결 해제
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # WebSocket으로부터 메시지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        # 방 그룹에 단순 메시지 보내기
        if action == "message":
            message = text_data_json["message"]
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

        # start 버튼 클릭 시
        elif action == "start":
            await self.action_start(self.room_name)
            room_data = await self.get_room_data(self.room_name)
            text = f"{self.scope['user'].username} has started the game."
        
        # ready 버튼 클릭 시
        elif action == "ready":
            await self.action_ready(self.room_name)
            room_data = await self.get_room_data(self.room_name)
            text = f"{self.scope['user'].username} is ready."

        # 방 그룹에 메시지 보내기
        message = {
            "action": action,
            "text": text,
            "room_data": room_data,
        }
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
        await await self.send(text_data=json.dumps({"message": message}))










    @database_sync_to_async
    def get_room_data(self, room_name):
        try:
            room = Room.objects.get(pk=room_name)
            serializer = RoomSerializer(room)
            return serializer.data
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def action_join(self, room_name, username):
        room = Room.objects.get(pk=room_name)
        room.players.append(username)
        room.current_participants += 1
        room.save()

    @database_sync_to_async
    def action_leave(self, room_name, username):
        room = Room.objects.get(pk=room_name)
        room.players.remove(username)
        room.current_participants -= 1
        room.ready_reset()
        room.save()

    @database_sync_to_async
    def action_start(self, room_name):
        room = Room.objects.get(pk=room_name)
        room.isPlaying = True
        room.save()

    @database_sync_to_async
    def action_ready(self, room_name):
        room = Room.objects.get(pk=room_name)
        room.ready_participants += 1
        room.save()
