import json
from channels.generic.websocket import AsyncWebsocketConsumer
from room.models import Room
from room.serializers import RoomSerializer
from channels.db import database_sync_to_async
# ValidationError
from rest_framework.exceptions import ValidationError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # 방 그룹에 참여하기
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 데이터베이스에서 방 데이터 가져오기
        room_data = await self.get_room_data(self.room_name)

        # 방 그룹에 연결 메시지와 함께 방 데이터 보내기
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "chat.message",
            "message": json.dumps(room_data),
        },
        )
            
        await self.accept()

    async def disconnect(self, close_code):
        # 데이터베이스에서 방 데이터 가져오기
        room_data = await self.get_room_data(self.room_name)

        # 방 그룹에 연결 해제 메시지와 함께 방 데이터 보내기
        if room_data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": json.dumps(room_data),
                },
            )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # WebSocket으로부터 메시지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # json에 command가 있는지 확인
        if "command" in text_data_json:
            command = text_data_json["command"]
            room_data = await self.put_ready(self.room_name)

            # 방 그룹에 연결 해제 메시지와 함께 방 데이터 보내기
            if room_data:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat.message",
                        "message": json.dumps(room_data),
                    },
                )
            return

        message = text_data_json["message"]

        # 방 그룹에 메시지 보내기
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # 방 그룹으로부터 메시지 받기
    async def chat_message(self, event):
        message = event["message"]

        # WebSocket으로 메시지 보내기
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_room_data(self, room_name):
        try:
            room = Room.objects.select_related().get(pk=room_name)
            serializer = RoomSerializer(room)
            return serializer.data
        except Room.DoesNotExist:
            return None
    
    @database_sync_to_async
    def put_ready(self, room_name):
        try:
            room = Room.objects.get(pk=room_name)
            room.get_ready()
            serializer = RoomSerializer(room)
            return serializer.data
        except Exception as e:
            print(e)
            return None