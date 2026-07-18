from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # после регистрации перенаправляем на логин

    def form_valid(self, form):
        user = form.save()
        # Отправка приветственного письма
        subject = 'Добро пожаловать!'
        message = f'Здравствуйте, {user.email}!\n\nВы успешно зарегистрировались на нашем сайте.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')  # после входа на главную


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['avatar', 'phone_number', 'country']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect('catalog:home')


from django.shortcuts import render

# Create your views here.
