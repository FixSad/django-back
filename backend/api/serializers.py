from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'age', 'education', 'specialty', 'residence',
            'height', 'weight', 'dominant_hand', 'diseases', 'smoking',
            'alcohol', 'sport', 'insomnia', 'current_mood', 'gamer'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'age', 'education', 'specialty']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            age=validated_data.get('age'),
            education=validated_data.get('education'),
            specialty=validated_data.get('specialty'),
        )
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user