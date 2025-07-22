# bookings/tests/test_views.py
from datetime import date, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from Hotel.models import Hotel, Room, RoomType
from .models import Booking, BookingRoom

User = get_user_model()


class BookingCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.other = User.objects.create_user(username="bob", password="pass")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", address="Addr", description="Desc", rating=4.5,
            city="City", image="images/x.jpg"
        )
        self.room = Room.objects.create(
            hotel=self.hotel, type=RoomType.SINGLE,
            price_per_night=100, is_available=True,
            image="images/r.jpg"
        )
        self.client = Client()

        self.url = reverse('room-book', kwargs={'pk': self.room.pk})
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after = self.today + timedelta(days=2)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_get_booking_form(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.get(self.url, {
            'check_in': self.today.isoformat(),
            'check_out': self.tomorrow.isoformat()
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Booking room")

    def test_conflict_booking_shows_error(self):
        existing = Booking.objects.create(
            customer=self.user,
            check_in=self.today,
            check_out=self.tomorrow,
            total_price=100
        )
        BookingRoom.objects.create(booking=existing, room=self.room)

        self.client.login(username="alice", password="pass")
        resp = self.client.post(self.url + f"?check_in={self.today}&check_out={self.tomorrow}", {
            'check_in': self.today.strftime('%d-%m-%Y'),
            'check_out': self.tomorrow.strftime('%d-%m-%Y'),
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "This room has been booked already for these dates.")
        self.assertEqual(Booking.objects.count(), 1)

    def test_successful_booking_creates_and_redirects(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.post(self.url + f"?check_in={self.today}&check_out={self.tomorrow}", {
            'check_in': self.today.strftime('%d-%m-%Y'),
            'check_out': self.tomorrow.strftime('%d-%m-%Y'),
        })
        self.assertEqual(resp.status_code, 302)
        booking = Booking.objects.latest('pk')
        self.assertEqual(booking.customer, self.user)
        self.assertEqual(booking.check_in, self.today)
        self.assertEqual(booking.check_out, self.tomorrow)
        self.assertRedirects(resp, reverse('booking-detail', kwargs={'pk': booking.pk}))


class BookingDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.other = User.objects.create_user(username="bob", password="pass")
        self.booking = Booking.objects.create(
            customer=self.user, check_in=date.today(),
            check_out=date.today()+timedelta(days=1),
            total_price=100
        )
        self.room = Room.objects.create(
            hotel=Hotel.objects.create(
                name="H",address="A",description="D",rating=5,city="C",image="i.jpg"
            ),
            type=RoomType.SINGLE,
            price_per_night=100, is_available=True,
            image="r.jpg"
        )
        BookingRoom.objects.create(booking=self.booking, room=self.room)
        self.url = reverse('booking-detail', kwargs={'pk': self.booking.pk})

    def test_owner_can_view(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f"Booking by")

    def test_other_user_gets_404(self):
        self.client.login(username="bob", password="pass")
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 404)


class BookingAPISetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.staff = User.objects.create_user(username="admin", password="pass", is_staff=True)
        # дві броні для різних користувачів
        self.b1 = Booking.objects.create(
            customer=self.user, check_in=date.today(),
            check_out=date.today()+timedelta(days=1),
            total_price=100
        )
        self.b2 = Booking.objects.create(
            customer=self.staff, check_in=date.today(),
            check_out=date.today()+timedelta(days=2),
            total_price=200
        )
        self.client = APIClient()


    def test_list_bookings_staff(self):
        self.client.login(username="admin", password="pass")
        resp = self.client.get(reverse('booking-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        pks = {item['id'] for item in resp.json()}
        self.assertTrue(self.b1.pk in pks and self.b2.pk in pks)

    def test_create_booking_via_api(self):
        self.client.login(username="alice", password="pass")
        data = {
            'customer_id': self.user.pk,
            'check_in': date.today().isoformat(),
            'check_out': (date.today()+timedelta(days=1)).isoformat(),
            'total_price': 150
        }
        resp = self.client.post(reverse('booking-list'), data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(customer=self.user, total_price=150).exists())

    def test_bookingroom_list(self):
        room = Room.objects.create(
            hotel=Hotel.objects.create(
                name="H2",address="A2",description="D2",rating=4,city="C2",image="i2"
            ),
            type=RoomType.DOUBLE, price_per_night=120,
            is_available=True, image="r2"
        )
        br = BookingRoom.objects.create(booking=self.b1, room=room)

        self.client.login(username="alice", password="pass")
        resp = self.client.get(reverse('bookingroom-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # переконаємось, що повернувся лише br
        items = resp.json()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['id'], br.pk)
