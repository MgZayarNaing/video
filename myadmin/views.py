from django.shortcuts import render
from django.contrib.auth import get_user_model

def dashboard_view(request):
    return render(request, 'dashboard.html')

def user_list(request):
    CustomUser = get_user_model()
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})