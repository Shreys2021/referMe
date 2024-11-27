from django.urls import path
from .views import register_user, login_user,register_form,login_form,home_page,referral_users,logout_user

urlpatterns = [
      path('registerform/',register_form, name='register_form'),
    path('register/', register_user, name='register_user'),
    path('loginform/', login_form, name='login_form'),
     path('login/',  login_user, name='login_user'),
     path('referrals/', referral_users, name='referrals'),
     path('logout/', logout_user, name='logout_user'),
]