from django.contrib import admin
from mhackspace.register.models import RegisteredUser


@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'created_at')
