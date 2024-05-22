from django.urls import path
from . import views
from .views import user_list


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', user_list, name='user_list'),
]
