from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from datetime import datetime
from .models import Hotel, RoomType, Room, HotelReview
from .forms import ReviewForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .serializers import HotelSerializer, RoomSerializer
from rest_framework import generics, permissions, viewsets
from .forms import SearchForm


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel-list.html'
    context_object_name = 'hotels'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        form = SearchForm(self.request.GET)
        if not form.is_valid():
            print(form.errors)
            
        if form.is_valid():
            cd = form.cleaned_data
            if cd['city']:
                qs = qs.filter(city__icontains=cd['city'])

            if cd.get('min_price') is not None:
                qs = qs.filter(room__price_per_night__gte=cd['min_price'])
            if cd.get('max_price') is not None:
                qs = qs.filter(room__price_per_night__lte=cd['max_price'])
            qs = qs.distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET)
        return ctx


class HotelDetailView(FormMixin, DetailView):
    model = Hotel
    template_name = 'hotels/hotel-detail.html'
    context_object_name = 'hotel'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('hotel-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)

        hotel = self.object
        check_in_str = self.request.GET.get('check_in')
        check_out_str = self.request.GET.get('check_out')

        rooms_qs = hotel.room_set.all()

        if check_in_str and check_out_str:
            try:
                ci = datetime.strptime(check_in_str, '%d-%m-%Y').date()
                co = datetime.strptime(check_out_str, '%d-%m-%Y').date()

                rooms_qs = rooms_qs.exclude(bookingroom__booking__check_in__lt = co,
                                          bookingroom__booking__check_out__gt = ci,)
            except ValueError:
                pass

        ctx['reviews'] = hotel.reviews.select_related('author')

        if self.request.user.is_authenticated:
            ctx['has_review'] = hotel.reviews.filter(author=self.request.user).exists()
        else:
            ctx['has_review'] = False
        
        ctx['available_rooms'] = rooms_qs.distinct()
        ctx['check_in'] = check_in_str
        ctx['check_out'] = check_out_str
        ctx['review_form'] = ctx.get('form') or self.get_form()
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.author = request.user
            form.instance.hotel = self.object
            form.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'hotels/room-detail.html'
    context_object_name = 'room'


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('hotel')
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

