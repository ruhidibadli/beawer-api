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
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=75)
    country = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=50, required=True)
    password2 = serializers.CharField(max_length=50, required=True)
    interested_with = CategorySerializer(many=True, required=False)
    user_type = serializers.ChoiceField(choices=USER_TYPES)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'country', 'interested_with', 'user_types', 'title', 'description')


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

