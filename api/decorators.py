# myapp/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.shortcuts import render

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_email'):
           return render(request, 'login.html', {'error': 'You must log in to access this page.'})
        return view_func(request, *args, **kwargs)
    return wrapper
