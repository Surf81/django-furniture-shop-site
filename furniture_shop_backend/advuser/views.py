from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from advuser.forms import EmailLoginForm, SignupForm, UpdateUserForm, ChangePasswordForm
from advuser.models import AdvancedUser


from django.contrib.auth.mixins import LoginRequiredMixin

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
        email = self.request.user if self.request.user.is_authenticated else None
        email = form.cleaned_data.get('email', email)
        if email:
            self.new_user = authenticate(email=email,
                                password=form.cleaned_data['password1'],
                                    )
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)        
        if hasattr(self, "new_user"):
            login(request, self.new_user)        
        return response


class SignupView(AutoAuthorizationMixin, CreateView):
    model = AdvancedUser
    form_class = SignupForm
    template_name = "advuser/register.html"
    success_url = reverse_lazy("auth:register_done")
    

class RegisterDoneView(TemplateView):
    template_name = 'advuser/register_done.html'


class UpdateUserView(UpdateView):
    model = AdvancedUser
    form_class = UpdateUserForm
    template_name = "advuser/update.html"
    success_url = reverse_lazy("auth:update_done")


class UpdateUserDoneView(TemplateView):
    template_name = 'advuser/update_done.html'


def done():
    return reverse_lazy("auth:password_change_done")


class ChangePasswordView(LoginRequiredMixin, AutoAuthorizationMixin, UpdateView):
    model = AdvancedUser
    form_class = ChangePasswordForm
    template_name = "advuser/password_change.html"
    success_url = done()


class ChangePasswordDoneView(TemplateView):
    template_name = 'advuser/password_change_done.html'
