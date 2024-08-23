from django.urls import path
from .views import RoomList, RoomCreate, room_detail, join_room, leave_room, RoomDelete, gameStart

urlpatterns = [
    path('room/', RoomList.as_view(), name='room-list'),
    path('room/create/', RoomCreate.as_view(), name='room-create'),
    path('room/<int:pk>/', room_detail, name='room-detail'),
    path('room/<int:pk>/join/', join_room, name='room-join'),
    path('room/<int:pk>/leave/', leave_room, name='room-leave'),
    path('room/<int:pk>/delete/', RoomDelete.as_view(), name='room-delete'),
    path('room/<int:pk>/start/', gameStart, name='game-start'),
]
