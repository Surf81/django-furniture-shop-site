from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.core.signing import BadSignature
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from advuser.forms import EmailLoginForm, SignupForm, UpdateUserForm
from advuser.models import AdvancedUser

from .utilities import signer


class EmailLoginView(LoginView):
    form_class = EmailLoginForm
    template_name = "advuser/login.html"    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_order'] = ("email", "password")
        return kwargs


class LogoutView(LogoutView):
    template_name = "advuser/logout_done.html"    


class AutoAuthorizationMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, "Спасибо за регистрацию. Вход в ваш профиль выполнен автоматически")
        email = form.cleaned_data['email']
        password=form.cleaned_data['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response


class SignupView(AutoAuthorizationMixin, CreateView):
    """Форма регистрации пользователя
    """
    model = AdvancedUser
    form_class = SignupForm
    template_name = "advuser/register.html"
    success_url = reverse_lazy("auth:register_done")

    def form_valid(self, form):
        messages.success(self.request, "Успешная регистрация!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Что-то пошло не так! Попробуйте еще раз")
        self.success_url = reverse_lazy("auth:signup")
        return super().form_invalid(form)
    

class RegisterDoneView(TemplateView):
    """Экран сообщения об успешной регистрации
    """
    template_name = 'advuser/register_done.html'


def user_activate(request, sign):
    """Обработчик перехода по ссылке активации учетной записи
    """
    try:
        email = signer.unsign(sign)
    except BadSignature:
        messages.error(request, "Код активации не верный!")
        return render(request, 'advuser/bad_signature.html')
    
    user = get_object_or_404(AdvancedUser, email=email)
    if user.is_activated:
        messages.warning(request, "Повторная попытка активации!")
        template = 'advuser/user_is_activated.html'
    else:
        messages.success(request, "Активация прошла успешно!")
        template = 'advuser/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """Форма изменения данных пользователя
    """
    model = AdvancedUser
    form_class = UpdateUserForm
    template_name = "advuser/update.html"
    success_url = reverse_lazy("auth:update_done")

    def setup(self, request, *args, **kwargs):
        answer = super().setup(request, *args, *kwargs)
        self.user_id = self.request.user.id
        return answer

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk = self.user_id)
    
    def form_valid(self, form):
        messages.success(self.request, "Данные изменены!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Что-то пошло не так!")
        self.success_url = reverse_lazy("auth:update")
        return super().form_invalid(form)


class UpdateUserDoneView(TemplateView):
    """Экран сообщения об успешном обновлении данных пользователя
    """
    template_name = 'advuser/update_done.html'


class ChangePasswordView(PasswordChangeView):
    """Форма изменения пароля пользователя
    """
    model = AdvancedUser
    template_name = "advuser/password_change.html"
    success_url = reverse_lazy("auth:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Пароль изменен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Что-то пошло не так! Попробуйте еще раз")
        self.success_url = reverse_lazy("auth:password_change")
        return super().form_invalid(form)


class ChangePasswordDoneView(TemplateView):
    """Экран сообщения об успешном изменении пароля пользователя
    """
    template_name = 'advuser/password_change_done.html'
