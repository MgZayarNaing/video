from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import logout
from django.utils import timezone 

User = get_user_model()

# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already exists'})
            elif User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
            elif User.objects.filter(phone_number=phone_number).exists():
                return render(request, 'register.html', {'error': 'Phone number already exists'})
            else:
                try:
                    user = User.objects.create(
                        username=username,
                        email=email,
                        phone_number=phone_number,
                        password=make_password(password)
                    )
                    user.is_active = False  # Admin လက်ခံမှ active ဖြစ်ဖို့အတွက်
                    user.save()
                    return redirect('login')
                except IntegrityError:
                    return render(request, 'register.html', {'error': 'An error occurred. Please try again.'})
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    else:
        return render(request, 'register.html')

# User Login
def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate using email or username
        user = None
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                pass
        
        if user is not None and user.check_password(password) and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or account not activated.'})
    else:
        return render(request, 'login.html')
    
# User Login
def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate using email or username
        user = None
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                pass
        
        if user is not None and user.check_password(password) and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or account not activated.'})
    else:
        return render(request, 'login.html')

# Logout view function
def user_logout(request):
    if request.user.is_authenticated:
        request.user.last_logout = timezone.now()
        request.user.save(update_fields=['last_logout'])
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')