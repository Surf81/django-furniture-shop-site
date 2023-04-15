from django.shortcuts import render
from django.contrib.auth.views import LoginView

from advuser.forms import EmailLoginForm, SignupForm



class EmailLoginView(LoginView):
    form_class = EmailLoginForm
    template_name = "advuser/login.html"    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_order'] = ("email", "password")
        return kwargs



class SignupView:

    form_class = SignupForm

    def generate_username(self, form):
        username = form.cleaned_data["email"]
        return username

    def after_signup(self, form):
        # do something
        super(SignupView, self).after_signup(form)