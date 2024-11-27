from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile_number', 'city', 'referral_code', 'password']

    def create(self, validated_data):
        # Here, we would ideally hash the password before saving it
        user = User.objects.create(**validated_data)
        return user
