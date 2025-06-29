from rest_framework import serializers
from .models import Booking, BookingRoom
from Customer.serializers import CustomUserSerializer
from Hotel.serializers import RoomSerializer
from Customer.models import Customer
from Hotel.models import Room


class BookingRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True)

    class Meta:
        model = BookingRoom
        fields = ['id', 'booking', 'room', 'room_id']


class BookingSerializer(serializers.ModelSerializer):
    customer = CustomUserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )
    # Вкладені бронь-кімнати
    booking_rooms = BookingRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'customer', 'customer_id',
            'check_in',
            'check_out',
            'total_price',
            'booking_rooms',
        ]



