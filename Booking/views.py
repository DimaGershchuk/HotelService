from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView
from rest_framework import viewsets, permissions
from django.urls import reverse
from Hotel.models import Room
from .models import Booking, BookingRoom
from .serializers import BookingRoomSerializer, BookingSerializer
from .forms import BookingForm
from django.shortcuts import get_object_or_404
from django.contrib import messages


class BookingCreateView(LoginRequiredMixin, FormView):
    template_name = 'bookings/booking-form.html'
    form_class = BookingForm

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=kwargs['pk'])
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')

        if not (check_in and check_out):
            messages.warning(
                request,
                "First of all chose your filters."
            )
            return redirect(reverse('hotel-list'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        ctx['room'] = self.room
        ctx['check_in']  = self.request.GET.get('check_in')
        ctx['check_out'] = self.request.GET.get('check_out')
        ctx['adults'] = self.request.GET.get('adults')
        return ctx

    def form_valid(self, form):
        cd = form.cleaned_data
        ci, co = cd['check_in'], cd['check_out']
        nights = (cd['check_out'] - cd['check_in']).days
        total = nights * self.room.price_per_night
        customer_obj = self.request.user

        conflict = Booking.objects.filter(bookingroom__room=self.room, check_in__lt=co, check_out__gt=ci,).exists()

        if conflict:
            form.add_error(None, "This room has been booked already for these dates.")
            return self.form_invalid(form)

        booking = Booking.objects.create(customer=customer_obj,
                                         check_in=cd['check_in'],
                                         check_out=cd['check_out'],
                                         total_price=total
                                         )
        BookingRoom.objects.create(booking=booking, room=self.room)
        return redirect('booking-detail', pk=booking.pk)


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking-detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(customer=user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer=user)


class BookingRoomViewSet(viewsets.ModelViewSet):
    queryset = BookingRoom.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BookingRoom.objects.all()
        return BookingRoom.objects.filter(booking__customer=user)
