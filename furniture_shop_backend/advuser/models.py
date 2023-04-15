from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.utils.translation import gettext_lazy as _


class AdvancedUserManager(UserManager):
    def get_by_natural_keys(self, **kwargs):
        if 'email' in kwargs:
            return self.get(**{self.model.EMAIL_FIELD: kwargs['email']})
        else:
            return self.get(**{self.model.USERNAME_FIELD: kwargs['username']})
     

class AdvancedUser(AbstractUser):
    is_activated = models.BooleanField('прошел активацию', default=True, db_index=True)
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True,
        validators=[validators.EmailValidator],
        error_messages={
            "unique": "Пользователь с таким email уже существует",
        },
    )

    objects = AdvancedUserManager()

    EMAIL_FIELD = "email"

    class Meta(AbstractUser.Meta):
        pass
