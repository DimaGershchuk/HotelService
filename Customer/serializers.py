from rest_framework import serializers
from .models import Customer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'age', 'tel_number']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'age', 'tel_number', 'password']

    def create(self, validated_data):
        user = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            age=validated_data['age'],
            tel_numer=validated_data['tel_number'],
            password=validated_data['password']
        )
        return user