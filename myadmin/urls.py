from django.urls import path
from .views import toggle_active, toggle_staff, delete_user, update_user, dashboard_view, user_list

urlpatterns = [
    path('toggle-active/<uuid:user_id>/', toggle_active, name='toggle_active'),
    path('toggle-staff/<uuid:user_id>/', toggle_staff, name='toggle_staff'),
    path('delete-user/<uuid:user_id>/', delete_user, name='delete_user'),
    path('update-user/<uuid:user_id>/', update_user, name='update_user'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('users/', user_list, name='user_list'),
]
