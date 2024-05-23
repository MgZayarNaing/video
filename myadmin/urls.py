from django.urls import path
from .views import *

urlpatterns = [
    path('toggle-active/<uuid:user_id>/', toggle_active, name='toggle_active'),
    path('toggle-staff/<uuid:user_id>/', toggle_staff, name='toggle_staff'),
    path('delete-user/<uuid:user_id>/', delete_user, name='delete_user'),
    path('update-user/<uuid:user_id>/', update_user, name='update_user'),
    path('users/<uuid:user_id>/', user_detail, name='user_detail'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('users/', user_list, name='user_list'),

    path('category/',category_list, name='category_list'),
    path('category/create/', create_category, name='create_category'),
    path('delete_category/<uuid:category_id>/',delete_category, name='delete_category'),
    path('category_detail/<uuid:category_id>/', category_detail, name='category_detail'),
    path('update_category/<uuid:category_id>/',update_category, name='update_category'),

    path('videos/',video_list, name='video_list'),
    path('videos/create/', create_video, name='create_video'),
    path('videos/<uuid:video_id>/',video_detail, name='video_detail'),
    path('videos/<uuid:video_id>/update/',update_video, name='update_video'),
    path('videos/<uuid:video_id>/delete/',delete_video, name='delete_video'),
]
