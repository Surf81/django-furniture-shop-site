from django.contrib import admin
import datetime

from .models import AdvancedUser
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')
send_activation_notifications.short_description = 'Отправить письма с требованиями активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('treedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'treedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_activate=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(week=1)
            return queryset.filter(is_activate=False, is_activated=False, date_joined__date__lt=d)


@admin.register(AdvancedUser)
class AdvancedUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = ('email',
              ('first_name', 'last_name'),
              ('is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('username', 'last_login', 'date_joined')
    actions = (send_activation_notifications,)

    def save_model(self, request, obj, form, change):
        obj.username = obj.email
        return super().save_model(request, obj, form, change)