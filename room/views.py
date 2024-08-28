from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer, RoomCreateSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        if Room.objects.filter(players__contains=[username]).exists():
            room = Room.objects.get(players__contains=[username])
            room.leave(username)
        return self.create(request, *args, **kwargs)

class RoomDetail(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDelete(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer




# TODO:


# 유저 0명일 때 방 삭제되는 이슈(새로고침 시)
# 소켓 DB 역할 나누기


# 게임 레디 상태 추가하기
# env 파일 만들기
# cors 설정
# 방 중복 참여 어떻게 방지할 것인가? 모든 방 순회하면서 확인하기로.
# 방 만들때 해당 유저가 방에 참가하도록. player1 = user
# swagger 사용해보기
# """
