from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from users.models import CustomUser
import json 
from django.utils import timezone
from datetime import timedelta
from .models import VisitorLog
from django.db.models import Sum 
from django.contrib.auth.models import Group
from django.contrib import messages
from myapp.models import *
import ffmpeg

import os


User = get_user_model()

@csrf_exempt
def toggle_active(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            data = json.loads(request.body)
            user.is_active = data.get('is_active', False)
            user.save(update_fields=['is_active'])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def toggle_staff(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            data = json.loads(request.body)
            user.is_staff = data.get('is_staff', False)
            user.save(update_fields=['is_staff'])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age') or None  # Ensure age is None if not provided
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST

        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.age = age
        user.gender = gender
        user.address = address
        user.is_active = is_active
        user.is_staff = is_staff
        
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, 'User details updated successfully!')
        return redirect('user_list')
    
    return render(request, 'update_user.html', {'user': user})

def dashboard_view(request):
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)

    total_users = CustomUser.objects.count()
    online_users = CustomUser.objects.filter(last_login__gte=ten_minutes_ago).count()
    offline_users = total_users - online_users

    user_growth = calculate_user_growth()
    daily_visitors, daily_visitor_growth = calculate_daily_visitors()
    total_visitors, total_visitor_growth = calculate_total_visitors()
    total_groups = Group.objects.count() 
    user_count = CustomUser.objects.count()
    is_staff = CustomUser.objects.filter(is_staff=True).count()
    is_active = CustomUser.objects.filter(is_active=True).count()
    
    total_categories = Category.objects.count()
    total_videos = Video.objects.count()

    return render(request, 'dashboard.html', {
        'total_users': total_users,
        'online_users': online_users,
        'offline_users': offline_users,
        'user_growth': user_growth,
        'daily_visitors': daily_visitors,
        'daily_visitor_growth': daily_visitor_growth,
        'total_visitors': total_visitors,
        'total_visitor_growth': total_visitor_growth,
        'total_groups': total_groups,
        'user_count': user_count,
        'total_active_users': is_active,
        'total_staff_users': is_staff,
        'total_categories': total_categories,
        'total_videos': total_videos,
    })


def calculate_user_growth():
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)
    
    current_month_count = CustomUser.objects.filter(date_joined__gte=one_month_ago).count()
    previous_month_count = CustomUser.objects.filter(date_joined__lt=one_month_ago, date_joined__gte=one_month_ago - timedelta(days=30)).count()
    
    if previous_month_count == 0:
        growth_percentage = 100
    else:
        growth_percentage = ((current_month_count - previous_month_count) / previous_month_count) * 100

    status = 'up' if growth_percentage >= 0 else 'down'
    
    return {
        'percentage': abs(growth_percentage),
        'status': status
    }

def calculate_daily_visitors():
    now = timezone.now()
    today_start = timezone.make_aware(timezone.datetime.combine(now.date(), timezone.datetime.min.time()))
    yesterday_start = today_start - timedelta(days=1)
    
    daily_visitors = CustomUser.objects.filter(last_login__gte=today_start).count()
    yesterday_visitors = CustomUser.objects.filter(last_login__gte=yesterday_start, last_login__lt=today_start).count()
    
    if yesterday_visitors == 0:
        growth_percentage = 100
    else:
        growth_percentage = ((daily_visitors - yesterday_visitors) / yesterday_visitors) * 100

    status = 'up' if growth_percentage >= 0 else 'down'
    
    # Save the daily visitors count
    visitor_log, created = VisitorLog.objects.get_or_create(date=today_start.date())
    visitor_log.count = daily_visitors
    visitor_log.save()

    return daily_visitors, {
        'percentage': abs(growth_percentage),
        'status': status
    }

def calculate_total_visitors():
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)
    
    total_visitors = VisitorLog.objects.aggregate(total=Sum('count'))['total'] or 0
    current_month_visitors = VisitorLog.objects.filter(date__gte=one_month_ago).aggregate(total=Sum('count'))['total'] or 0
    previous_month_visitors = VisitorLog.objects.filter(date__lt=one_month_ago, date__gte=one_month_ago - timedelta(days=30)).aggregate(total=Sum('count'))['total'] or 0
    
    if previous_month_visitors == 0:
        growth_percentage = 100
    else:
        growth_percentage = ((current_month_visitors - previous_month_visitors) / previous_month_visitors) * 100
    
    status = 'up' if growth_percentage >= 0 else 'down'

    return total_visitors, {
        'percentage': abs(growth_percentage),
        'status': status
    }

def user_list(request):
    CustomUser = get_user_model()
    users = CustomUser.objects.all().order_by('-created_at')
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_detail.html', {'user': user})


def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'category_list.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Name is required.')
    return render(request, 'create_category.html')


@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return JsonResponse({'status': 'success'}, status=200, content_type='application/json')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400, content_type='application/json')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400, content_type='application/json')

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category_detail.html', {'category': category})

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Name is required.')

    return render(request, 'update_category.html', {'category': category})

def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'video_list.html', {'videos': videos})

@csrf_exempt
def create_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video_file')

        if not video_file:
            return JsonResponse({'error': 'Invalid file'}, status=400)
        
        try:
            # Save uploaded file
            video = Video.objects.create(
                category_id=request.POST.get('category'),
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                video_file=video_file,
                user=request.user
            )
            
            return JsonResponse({'message': 'Video uploaded successfully', 'video_id': video.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Failed to upload video', 'details': str(e)}, status=500)
    else:
        return render(request, 'create_video.html', {'categories': Category.objects.all()})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'video_detail.html', {'video': video})

@csrf_exempt
def update_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        video_file = request.FILES.get('video_file')

        video.name = name
        video.description = description
        video.category = category

        if video_file:
            video.video_file = video_file

        video.save()
        messages.success(request, 'Video updated successfully!')
        return redirect('video_list')

    return render(request, 'update_video.html', {'video': video, 'categories': Category.objects.all()})

@csrf_exempt
def delete_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

