from django.db import models
from Customer.models import Customer
from Hotel.models import Room


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.IntegerField()
    rooms = models.ManyToManyField(Room, through='BookingRoom', related_name='booked_in')

    def __str__(self):
        return f"By {self.customer} from {self.check_in} till {self.check_out}"


class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room} booked in {self.booking}"




