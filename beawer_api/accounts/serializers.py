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


class CategoryIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=75)
    password = serializers.CharField(max_length=50, required=True)
    interested_with = CategoryIDSerializer(many=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_TYPES)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False, format="%d.%m.%Y")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%d.%m.%Y")
    date_joined = serializers.DateTimeField(format="%d.%m.%Y")
    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'date_joined']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class EmployerSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateTimeField(format="%d.%m.%Y")
    user = UserSerializer(read_only=True)
    class Meta:
        model = Employer
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateTimeField(format="%d.%m.%Y")
    user = serializers.StringRelatedField()
    interested_with = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Applicant
        fields = '__all__'