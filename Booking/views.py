from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Booking, BookingRoom
from .serializers import BookingRoomSerializer, BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer__user=user)


class BookingRoomViewSet(viewsets.ModelViewSet):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BookingRoom.objects.all()
        return BookingRoom.objects.filter(booking__customer__user=user)
