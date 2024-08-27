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

    # current_participants가 0인 방 삭제
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        # for room in rooms:
        #     if room.current_participants == 0:
        #         room.delete()
        return self.list(request, *args, **kwargs)

class RoomCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        username = request.user.username
        if Room.objects.filter(players__contains=[username]).exists():
            raise ValidationError("Room already exists")
        return self.create(request, *args, **kwargs)

class RoomDetail(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDelete(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# @api_view(['PATCH'])
# def join_room(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#     except Room.DoesNotExist:
#         return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     username = request.user.username
#     if check_user_in_allroom(username):
#         return Response({'message': 'User is already in the room'}, status=status.HTTP_400_BAD_REQUEST)
#     room.add_player(username)
#     return Response({'message': 'User has joined the room'}, status=status.HTTP_200_OK)

# @api_view(['PATCH'])
# def leave_room(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#     except Room.DoesNotExist:
#         return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     room.remove_player(request.user.username)
#     room.ready_reset()
#     if room.current_participants == 0:
#         room.delete()
#     return Response({'message': 'User has left the room'}, status=status.HTTP_200_OK)


# @api_view(['PATCH'])
# def gameStart(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#     except Room.DoesNotExist:
#         return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     room.start_game()
#     return Response({'message': 'Game has started'}, status=status.HTTP_200_OK)


# @api_view(['PATCH'])
# def gameReady(request, pk):
#     try:
#         room = Room.objects.get(pk=pk)
#     except Room.DoesNotExist:
#         return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     username = request.user.username
#     if not room.user_in_room(username):
#         return Response({'message': 'User is not in the room'}, status=status.HTTP_400_BAD_REQUEST)
#     room.get_ready()
#     return Response({'message': 'someone is ready'}, status=status.HTTP_200_OK)

# User is already in the another room.

# def check_user_in_allroom(username):
#     rooms = Room.objects.all()
#     for room in rooms:
#         if room.user_in_room(username):
#             True
#     return False



# TODO:

# 소켓 DB 역할 나누기


# 게임 레디 상태 추가하기
# env 파일 만들기
# cors 설정
# 방 중복 참여 어떻게 방지할 것인가? 모든 방 순회하면서 확인하기로.
# 방 만들때 해당 유저가 방에 참가하도록. player1 = user
# swagger 사용해보기
# """
