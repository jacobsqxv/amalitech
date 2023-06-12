from django.contrib import admin

# Register your models here.
from .models import AccessKey, User

@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('access_key','procurement_date',)
    list_display = ('access_key', 'status', 'procurement_date', 'expiry_date')
    list_filter = ('status', 'expiry_date')
    search_fields = ('status',)

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')