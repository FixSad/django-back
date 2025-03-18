from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, TestNSI, TestResults


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'age', 'education', 'specialty', 'residence',
            'height', 'weight', 'dominant_hand', 'diseases', 'smoking',
            'alcohol', 'sport', 'insomnia', 'current_mood', 'gamer'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'age', 'education', 'specialty', 'residence',
            'height', 'weight', 'dominant_hand', 'diseases', 'smoking',
            'alcohol', 'sport', 'insomnia', 'current_mood', 'gamer'
        ]
        extra_kwargs = {
            'username': {'read_only': True}  # Имя пользователя нельзя менять
        }


class TestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResults
        fields = [
            'id', 'test', 'try_number',
            'number_all_answers', 'number_correct_answers',
            'complete_time', 'accuracy'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['user']
        return TestResults.objects.create(user=user, **validated_data)


class TestNSISerializer(serializers.ModelSerializer):
    class Meta:
        model = TestNSI
        fields = ['test_name', 'tittle_all', 'tittle_correct']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'age', 'education', 'specialty',
            'residence', 'height', 'weight', 'dominant_hand', 'diseases',
            'smoking', 'alcohol', 'sport', 'insomnia', 'current_mood', 'gamer'
        ]

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
            residence=validated_data.get('residence'),
            height=validated_data.get('height'),
            weight=validated_data.get('weight'),
            dominant_hand=validated_data.get('dominant_hand'),
            diseases=validated_data.get('diseases'),
            smoking=validated_data.get('smoking', False),
            alcohol=validated_data.get('alcohol', False),
            sport=validated_data.get('sport', False),
            insomnia=validated_data.get('insomnia', False),
            current_mood=validated_data.get('current_mood'),
            gamer=validated_data.get('gamer', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
