from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, LoginView, LogoutView, ProfileView, verify_view, generate_password_view

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<code>/', verify_view, name='verify'),
    path('generate_password/', generate_password_view, name='generate_password'),
]
