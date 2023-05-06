from django.apps import AppConfig
from django.dispatch import Signal

from .utilities import send_activation_notification


class AdvuserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "advuser"
    verbose_name = "пользователи"



user_registered = Signal()

def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registered.connect(user_registered_dispatcher)