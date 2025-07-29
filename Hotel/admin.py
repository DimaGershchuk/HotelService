from django.contrib import admin
from .models import Hotel, Room, RoomType, HotelReview

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(HotelReview)