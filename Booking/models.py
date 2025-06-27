from django.db import models
from Customer.models import Customer
from Hotel.models import Room


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.IntegerField()

    def __str__(self):
        return f"Booking by {self.customer}"


class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room {self.room} booked in {self.booking}"




