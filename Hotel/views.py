from django.shortcuts import render
from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomSerializer
from rest_framework import generics, permissions, viewsets


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('hotel')
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

