from django.contrib import admin
from django.contrib.gis import admin, forms
from django.contrib.gis.db import models
from .models import Location, LocationGeo, City
from .forms import AccountChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis import admin
from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import GEOSGeometry
from django.utils.safestring import mark_safe


class GoogleMapPointWidget(forms.OSMWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            try:
                point = GEOSGeometry(value)
                latitude = point.y
                longitude = point.x
                google_map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                return mark_safe(f'<a href="{google_map_url}" target="_blank">{value}</a>')
            except Exception as e:
                pass
        return super().render(name, value, attrs, renderer)


class LocationGeoAdmin(admin.OSMGeoAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GoogleMapPointWidget},
    }
    list_display = ('id', 'location', 'point')


admin.site.register(LocationGeo, LocationGeoAdmin)


class LocationAdmin(UserAdmin):
    form = AccountChangeForm
    add_fields = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password', 'password2',)}),
    )
    list_display = ('id', 'username', 'is_superuser', 'is_staff', 'is_active', 'created_date')
    ordering = None
    readonly_fields = ('created_date', )
    list_filter = ('created_date', 'is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_date',)}),
    )
    search_fields = ('username',)


admin.site.register(Location, LocationAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'location_geo']


admin.site.register(City, CityAdmin)
