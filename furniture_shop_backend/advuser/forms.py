from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst

from django.contrib.auth import authenticate, get_user_model

UserModel = get_user_model()


class EmailLoginForm(forms.Form):
    email = forms.EmailField(max_length=150,
                             label=_("Email address"),
                             widget=forms.TextInput(attrs={"autofocus": True,
                                                           "type": "email",
                                                           "autocomplete": "email"}))
    
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_email": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields["email"].max_length = email_max_length
        self.fields["email"].widget.attrs["maxlength"] = email_max_length
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_email"],
            code="invalid_login",
            params={"username": self.email_field.verbose_name},
        )


class SignupForm(forms.ModelForm):
    pass
