from django.db import models
from django.conf import settings
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


class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating  = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(max_length=2_000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['hotel', 'author'], name='unique_review_per_user')
        ]

    def __str__(self):
        return f'{self.hotel} – {self.rating}★ by {self.author}'





