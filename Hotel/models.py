from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    city = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(350, 350)],
        format='JPEG',
        options={'quality': 95}
    )

    def __str__(self):
        return self.name


class RoomType(models.TextChoices):
    SINGLE = 'For two person', 'Single bed'
    DOUBLE = 'For three and four', 'Two beds'
    SUITE = 'Suite', 'Luxe'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_name = models.CharField(default='Deluxe')
    type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.SINGLE,
                            verbose_name='Room type')
    price_per_night = models.IntegerField()
    is_available = models.BooleanField()

    image = models.ImageField(upload_to='images', blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(350, 350)],
        format='JPEG',
        options={'quality': 95}
    )

    def __str__(self):
        return f"Room {self.room_name} in hotel {self.hotel}"







