from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdvancedBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, email, password, request=None):
        credentials = {
            get_user_model().EMAIL_FIELD: email,
            'password': password
        }
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)    
    

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )