# hotel/tests/test_views.py
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from Hotel.models import Hotel, Room, RoomType
from Booking.models import Booking, BookingRoom

User = get_user_model()

class BaseDataMixin:
    def make_hotel(self, name='H', city='Kyiv', prices=(100, 200)):
        hotel = Hotel.objects.create(
            name=name,
            address='Addr', description='Desc',
            rating=4.5, city=city, image='images/1.jpg'
        )
        rooms = []
        for i, p in enumerate(prices, start=1):
            rooms.append(
                Room.objects.create(
                    hotel=hotel,
                    type=RoomType.SINGLE,
                    price_per_night=p,
                    is_available=True, image='room.jpg',
                )
            )
        return hotel, rooms


# ------------------------------------------------------------------ #
#   CLASS‑BASED TEMPLATE VIEWS                                       #
# ------------------------------------------------------------------ #
class HotelListViewTests(BaseDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hotel1, _ = cls().make_hotel(name='Kyiv Hotel', city='Kyiv', prices=(100,))
        cls.hotel2, _ = cls().make_hotel(name='Lviv Hotel', city='Lviv', prices=(400,))
        cls.url = reverse('hotel-list')

    def test_list_without_filters(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Kyiv Hotel')
        self.assertContains(resp, 'Lviv Hotel')

    def test_filter_by_city(self):
        resp = self.client.get(self.url, {'city': 'Lviv'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Lviv Hotel')
        self.assertNotContains(resp, 'Kyiv Hotel')

    def test_filter_by_price_range(self):
        resp = self.client.get(self.url, {'min_price': 300, 'max_price': 500})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Lviv Hotel')
        self.assertNotContains(resp, 'Kyiv Hotel')