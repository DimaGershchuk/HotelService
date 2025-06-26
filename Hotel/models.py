from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=2)


class RoomType(models.TextChoices):
    SINGLE = 'Single', 'Одномісний'
    DOUBLE = 'Double', 'Двомісний'
    SUITE = 'Suite', 'Люкс'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.SmallIntegerField()
    type = models.CharField(max_length=10, choices=RoomType.choices, default=RoomType.SINGLE,
                            verbose_name='Room type')
    capacity = models.SmallIntegerField()
    price_per_night = models.IntegerField()
    is_available = models.BooleanField()



