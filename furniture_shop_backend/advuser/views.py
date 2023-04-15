from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from advuser.forms import EmailLoginForm, SignupForm
from advuser.models import AdvancedUser



class EmailLoginView(LoginView):
    form_class = EmailLoginForm
    template_name = "advuser/login.html"    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_order'] = ("email", "password")
        return kwargs



class SignupView(CreateView):
    model = AdvancedUser
    form_class = SignupForm
    template_name = "advuser/register.html"
    success_url = reverse_lazy("auth:register_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.new_user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'],
                                    )
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)        
        if hasattr(self, "new_user"):
            login(request, self.new_user)        
        return response
    

class RegisterDoneView(TemplateView):
    template_name = 'advuser/register_done.html'