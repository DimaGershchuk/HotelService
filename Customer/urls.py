from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterUser, LoginUser, logout_user, UserPasswordChange

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/password', UserPasswordChange.as_view(template_name='users/password_change.html'), name='password_change'),
    path('profile/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]