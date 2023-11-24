from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from teamwork_app.forms import LoginUserForm, RegisterUserForm


class RegisterView(CreateView):
    """
    Регистрация пользователей
    """

    form_class = RegisterUserForm
    template_name = "registration.html"
    permission_classes = []

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("main-menu")


class AuthView(LoginView):
    """
    Аунтификацуя пользователей
    """

    form_class = LoginUserForm
    template_name = "login.html"
    permission_classes = []

    def get_success_url(self):
        return reverse_lazy("main-menu")


def logout_user(request):
    """
    Выход из профиля
    """
    logout(request)
    return redirect("main-screen")


class SecureTemplateView(TemplateView):
    """
    Класс для блокировки доступа пользователей без аунтификации к страницам без вьюх
    """

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)
