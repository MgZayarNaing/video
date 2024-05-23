from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
from django.contrib import messages

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        # Check if any field is empty
        if not (username and email and phone_number and password and password2):
            messages.error(request, 'Please fill in all fields.')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('register')

        try:
            user = User.objects.create(
                username=username,
                email=email,
                phone_number=phone_number,
                password=make_password(password)
            )
            user.is_active = False  # Require admin approval
            user.save()
            messages.success(request, 'Your account has been created and is pending approval.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return redirect('register')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not (username_or_email and password):
            messages.error(request, 'Please enter both username/email and password.')
            return redirect('login')

        user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()

        if user and user.check_password(password) and user.is_active:
            login(request, user)
            return redirect('/myapp/')
        else:
            messages.error(request, 'Invalid credentials or account not activated.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        request.user.last_logout = timezone.now()
        request.user.save(update_fields=['last_logout'])
    logout(request)
    return redirect('login')
