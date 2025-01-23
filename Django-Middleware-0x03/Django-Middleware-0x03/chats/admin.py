from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message


class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'role')
    list_filter = ('role', 'created_at')
    ordering = ('-created_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
