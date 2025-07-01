from django.urls import path
from .views import BookingCreateView, BookingDetailView

urlpatterns = [
    path('room/<int:pk>/book/', BookingCreateView.as_view(), name='room-book'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]