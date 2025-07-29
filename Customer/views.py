from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import CustomUserCreationForm, LoginUserForm, PasswordChangeForm, ProfileForm
from rest_framework import viewsets, permissions, generics
from .models import Customer
from .serializers import CustomUserSerializer, CustomUserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from Booking.models import Booking

class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('hotel-list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('hotel-list')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "users/password_change_form.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = ProfileForm
    template_name = 'users/profile-edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = self.request.user 
        context["bookings"] = Booking.objects.filter(customer=user).select_related('customer').prefetch_related('rooms', 'rooms__hotel')
        return context
 
        

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer