from rest_framework import serializers
from .models import Employer, Applicant, Category
from django.contrib.auth.models import User


USER_TYPES = [
    ('Guest', 'Guest'),
    ('Employer', 'Employer'),
    ('Applicant', 'Applicant'),
]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=75)
    password = serializers.CharField(max_length=50, required=True)
    interested_with = CategorySerializer(many=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_TYPES)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'interested_with', 'user_types', 'title', 'description')


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%b, %d, %Y, %I:%M %p")
    date_joined = serializers.DateTimeField(format="%b, %d, %Y, %I:%M %p")
    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'date_joined']