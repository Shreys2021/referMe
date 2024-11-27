from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
import random
import string

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(
        max_length=10, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be exactly 10 digits.',
                code='invalid_mobile_number'
            )
        ]
    )
    city = models.CharField(max_length=50)
    referral_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_referral_code()

        # Hash the password before saving it
        self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
