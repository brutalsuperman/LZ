from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

UserAdmin.list_display += ('last_ip',)
admin.site.register(Profile, UserAdmin)
