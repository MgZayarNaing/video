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
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'

        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.is_active = is_active
        user.is_staff = is_staff

        user.save()
        return redirect('user_list')  # Adjust to the name of your user list view

    return render(request, 'update_user.html', {'user': user})

def dashboard_view(request):
    user_count = CustomUser.objects.count()
    user_growth = calculate_user_growth()
    daily_visitors, daily_visitor_growth = calculate_daily_visitors()
    total_visitors, total_visitor_growth = calculate_total_visitors()
    return render(request, 'dashboard.html', {
        'user_count': user_count,
        'user_growth': user_growth,
        'daily_visitors': daily_visitors,
        'daily_visitor_growth': daily_visitor_growth,
        'total_visitors': total_visitors,
        'total_visitor_growth': total_visitor_growth,
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
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
