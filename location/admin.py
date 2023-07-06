from django.contrib import admin
from .models import Location, LocationGeo
from .forms import AccountChangeForm
from django.contrib.auth.admin import UserAdmin


class LocationAdmin(UserAdmin):
    form = AccountChangeForm
    add_fields = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password', 'password2',)}),
    )
    list_display = ('id', 'username', 'city', 'lat', 'long', 'is_superuser',
                    'is_staff', 'is_active', 'created_date')
    ordering = None
    readonly_fields = ('created_date', )
    list_filter = ('created_date', 'is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'city', 'lat', 'long', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_date',)}),
    )
    search_fields = ('username',)


admin.site.register(Location, LocationAdmin)
admin.site.register(LocationGeo)
