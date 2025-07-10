import random
import string

from django.conf import settings
from django.contrib.auth.views import LogoutView as BaseLogoutView, LoginView as BaseLoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import RegisterForm, ProfileForm
from users.models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        user = form.save()
        user.verify_code = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 8)])
        user.is_active = False
        user.save()
        message = (f"Для завершения регистрации на портале ProductStore "
                   f"перейдите по ссылке http://127.0.0.1:8000/users/verify/{user.verify_code}")
        send_mail("Подтверждение регистрации", message, settings.EMAIL_HOST_USER, recipient_list=[user.email])
        return super().form_valid(form)


class ProfileView(UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


def verify_view(request, code):
    user = User.objects.filter(verify_code=code).first()
    if user is None:
        return render(request, 'users/verify_unsuccess.html')
    user.is_active = True
    user.save()
    return render(request, 'users/verify_success.html')


def generate_password_view(request):
    if request.method == 'GET':
        return render(request, 'users/enter_email.html')
    email = request.POST.get('email')
    password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 8)])
    message = f'Ваш новый пароль: {password}'
    user = User.objects.filter(email=email).first()
    if user is None:
        context = {'email': email}
        return render(request, 'users/generate_password_unsuccess.html', context=context)
    user.set_password(password)
    user.save()
    send_mail("Восстановление пароля на ProductStore", message, settings.EMAIL_HOST_USER,
              recipient_list=[email])
    return render(request, 'users/generate_password_success.html')

