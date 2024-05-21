from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
import phonenumbers
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_phone_number(number, region='MM'):
    try:
        phone_number = phonenumbers.parse(number, region)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("Invalid phone number for the given region")
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number format")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        region = request.POST.get('phone_region', 'MM')  # Default to 'MM' if not specified
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            validate_phone_number(phone_number, region)
        except ValidationError as e:
            return render(request, 'register.html', {'error': str(e)})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(phone_number=phone_number).exists():
            return render(request, 'register.html', {'error': 'Phone number already exists'})

        try:
            user = User.objects.create(
                username=username,
                email=email,
                phone_number=phone_number,
                password=make_password(password)
            )
            user.is_active = False  # Require admin approval
            user.save()
            return redirect('login')
        except IntegrityError:
            return render(request, 'register.html', {'error': 'An error occurred. Please try again.'})
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()

        if user and user.check_password(password) and user.is_active:
            login(request, user)
            return redirect('/myapp/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or account not activated.'})

    else:
        return render(request, 'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        request.user.last_logout = timezone.now()
        request.user.save(update_fields=['last_logout'])
    logout(request)
    return redirect('login')
