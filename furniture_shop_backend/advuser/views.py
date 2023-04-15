from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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


def user_activate(request, sign):
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
    template_name = 'advuser/update_done.html'


class ChangePasswordView(PasswordChangeView):
    model = AdvancedUser
    template_name = "advuser/password_change.html"
    success_url = reverse_lazy("auth:password_change_done")


class ChangePasswordDoneView(TemplateView):
    template_name = 'advuser/password_change_done.html'
