from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Hotel, RoomType, Room
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
        if form.is_valid():
            cd = form.cleaned_data
            if cd['city']:
                qs = qs.filter(city__icontains=cd['city'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET)
        return ctx


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel-detail.html'
    context_object_name = 'hotel'


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

