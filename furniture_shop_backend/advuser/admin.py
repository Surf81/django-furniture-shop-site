from django.contrib import admin

from advuser.models import AdvancedUser

@admin.register(AdvancedUser)
class AdvancedUserAdmin(admin.ModelAdmin):
    pass
