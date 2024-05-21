import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'email', 
        'username', 
        'is_active', 
        'is_staff', 
        'formatted_date_joined', 
        'formatted_last_login', 
        'formatted_last_logout', 
        'get_duration'
    ]
    readonly_fields = ['date_joined', 'last_login', 'last_activity', 'last_logout']
    actions = [export_as_csv]

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_activity', 'last_logout')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    def get_status(self, obj):
        if obj.last_activity:
            delta = timezone.now() - obj.last_activity
            if delta.seconds < 300:  # Considered online if active within the last 5 minutes
                return "Online"
        return "Offline"
    get_status.short_description = 'Status'

    def get_duration(self, obj):
        if obj.last_logout and obj.last_login:
            duration = obj.last_logout - obj.last_login
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{hours}:{minutes:02}:{seconds:02}'
        return "N/A"
    get_duration.short_description = 'Duration'

    def formatted_date_joined(self, obj):
        if obj.date_joined:
            return obj.date_joined.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"
    formatted_date_joined.short_description = 'Date Joined'

    def formatted_last_login(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"
    formatted_last_login.short_description = 'Last Login'

    def formatted_last_logout(self, obj):
        if obj.last_logout:
            return obj.last_logout.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"
    formatted_last_logout.short_description = 'Last Logout'

admin.site.register(CustomUser, CustomUserAdmin)
