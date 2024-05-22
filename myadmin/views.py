from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from users.models import CustomUser  # Change this to the correct app name
import json  # Add this import


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
    return render(request, 'dashboard.html')

def user_list(request):
    CustomUser = get_user_model()
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
