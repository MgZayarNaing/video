from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'id', 'username', 'email', 'phone_number', 'age', 'gender', 
        'address', 'is_active', 'is_staff', 'date_joined', 'last_login', 
        'last_activity', 'last_logout', 'formatted_phone_number', 
        'formatted_date_joined', 'formatted_last_login', 
        'formatted_last_logout', 'get_duration', 'get_status'
    ]
    list_filter = ['is_staff', 'is_active', 'gender']
    search_fields = ['username', 'email', 'phone_number']
    ordering = ['date_joined']
    readonly_fields = ['date_joined', 'last_login', 'last_activity', 'last_logout']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'age', 'gender', 'address', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_activity', 'last_logout')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 
                       'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
