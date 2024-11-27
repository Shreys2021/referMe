from django.shortcuts import render,HttpResponse
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .models import User
from .decorators import login_required

# Create your views here.

def home_page(request):
    if request.method == 'GET':
        return render(request, 'home.html') 

def register_form(request):
    if request.method == 'GET':
        return render(request, 'register.html')

def login_form(request):
    if request.method == 'GET':
        return render(request, 'login.html')

@api_view(['POST'])
def register_user(request):
  
    email = request.data.get('email')
    name = request.data.get('name')
    mobile_number = request.data.get('mobile_number')
    city = request.data.get('city')
    password = request.data.get('password')
    referral_code = request.data.get('referral_code')

   
    if not all([email, name, mobile_number, city, password]):
        return render(request, 'register.html', {'error': 'All fields except referral code are required.'})

    if len(mobile_number) != 10 or not mobile_number.isdigit():
        return render(request, 'register.html', {'error': 'Mobile number must be exactly 10 digits.'})
   
    if User.objects.filter(email=email).exists():
        return render(request, 'register.html', {'error': 'Email already exists. Please use a different email.'})
    if User.objects.filter(name=name).exists():
        return render(request, 'register.html', {'error': 'Name already exists. Please use a different name.'})
    if User.objects.filter(mobile_number=mobile_number).exists():
        return render(request, 'register.html', {'error': 'Mobile number already exists. Please use a different mobile number.'})

   
    referrer = None
    if referral_code:
        try:
            referrer = User.objects.get(referral_code=referral_code)
        except User.DoesNotExist:
            return render(request, 'register.html', {'error': 'Invalid referral code.'})

  
    user = User(
        email=email,
        name=name,
        mobile_number=mobile_number,
        city=city,
        password=password 
    )
    
   
    if referrer:
        user.referred_by = referrer

    user.save() 

    
    context = {
        'username': user.name,
        'referral_code': user.referral_code
    }
    return render(request, 'register_success.html', context)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    
    if not email or not password:
        return render(request, 'login.html', {'error': 'Invalid email or password.'})

  
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render(request, 'login.html', {'error': 'Invalid email or password.'})

  
    if not check_password(password, user.password):
        return render(request, 'login.html', {'error': 'Invalid email or password.'})

    request.session['user_email'] = user.email

  
    return render(request, 'login_success.html')


@login_required
def referral_users(request):
   
    user_email = request.session.get('user_email')

    if not user_email:
        return render(request, 'login.html', {'error': 'Please log in to view referrals.'})

 
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})

  
    referrals = User.objects.filter(referred_by=user)

    context = {
        'username': user.name,
        'referrals': referrals,
    }
    return render(request, 'referrals.html', context)


@login_required
def logout_user(request):
    request.session.flush() 
    return render(request, 'login.html', {'message': 'You have been logged out.'})
