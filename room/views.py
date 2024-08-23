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

    def perform_create(self, serializer):
        room = serializer.save()
        username = self.request.user.username
        room.add_player(username)


@api_view(['GET'])
def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['PATCH'])
def join_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
    username = request.user.username
    room.add_player(username)
    return Response({'message': 'User has joined the room'}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def leave_room(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
    username = request.user.username
    room.remove_player(username)
    if room.current_participants == 0:
        room.delete()
    return Response({'message': 'User has left the room'}, status=status.HTTP_200_OK)

class RoomDelete(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_destroy(self, instance):
        instance.delete()

@api_view(['PATCH'])
def gameStart(request, pk):
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND)
    room.start_game()
    return Response({'message': 'Game has started'}, status=status.HTTP_200_OK)



# TODO 방 중복 참여 어떻게 방지할 것인가? = 유저 데이터에 방 정보 저장?



# TODO 방 만들때 해당 유저가 방에 참가하도록. player1 = user
# TODO swagger 사용해보기