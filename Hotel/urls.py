from django.urls import path

from .views import HotelListView

urlpatterns = [
    path('hotel-list/', HotelListView.as_view(), name='hotel-list')
]