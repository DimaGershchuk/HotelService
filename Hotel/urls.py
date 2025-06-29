from django.urls import path

from .views import HotelListView, HotelDetailView, RoomDetailView

urlpatterns = [
    path('hotel-list/', HotelListView.as_view(), name='hotel-list'),
    path('hotel-detail/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('room-detail/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]