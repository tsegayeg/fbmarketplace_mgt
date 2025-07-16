# core/admin.py
from django.contrib import admin
from .models import User, FacebookAccount, DailyEntry

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

@admin.register(FacebookAccount)
class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ('fb_name', 'fb_email', 'phone')

@admin.register(DailyEntry)
class DailyEntryAdmin(admin.ModelAdmin):
    list_display = ('maker', 'fb_account', 'status')
    list_filter = ('status',)
