from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.core.signing import BadSignature
from django.utils.translation import gettext_lazy as _

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
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class SignupView(AutoAuthorizationMixin, CreateView):
    """Форма регистрации пользователя
    """
    model = AdvancedUser
    form_class = SignupForm
    template_name = "advuser/register.html"
    success_url = reverse_lazy("auth:register_done")
    

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
        return render(request, 'auth/bad_signature.html')
    
    user = get_object_or_404(AdvancedUser, email=email)
    if user.is_activated:
        template = 'auth/user_is_activated.html'
    else:
        template = 'auth/activation_done.html'
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


class ChangePasswordDoneView(TemplateView):
    """Экран сообщения об успешном изменении пароля пользователя
    """
    template_name = 'advuser/password_change_done.html'
