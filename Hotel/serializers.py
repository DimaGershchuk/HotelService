from rest_framework import serializers
from .models import Hotel, RoomType, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), source='hotel', write_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'hotel_id', 'type', 'type_display',
                  'price_per_night', 'is_available']