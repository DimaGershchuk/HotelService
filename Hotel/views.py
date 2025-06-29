from django.shortcuts import render
from django.views.generic import ListView

from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomSerializer
from rest_framework import generics, permissions, viewsets


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel-list.html'
    context_object_name = 'hotels'
    paginate_by = 10
    

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('hotel')
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

