from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Employer, Applicant, Category
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignUpSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import re
# Create your views here.




class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                try:
                    user = User.objects.get(email=email)
                except ObjectDoesNotExist:
                    return Response({'error':'User not found with given email!'}, status=status.HTTP_400_BAD_REQUEST)



                is_user = authenticate(username=user.username, password=password)

                if is_user:
                    return Response({'data':{'user_id':user.id}}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'The password is wrong!'}, status=status.HTTP_400_BAD_REQUEST)
                


            else:
                return Response({'error':'Entered data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)



class SignUpAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            country = serializer.validated_data.get('country')
            email = serializer.validated_data.get('email').lower()
            username = serializer.validated_data.get('username').lower()
            full_name = serializer.validated_data.get('full_name')
            password = serializer.validated_data.get('password')
            interested_with = serializer.validated_data.get('interested_with')
            user_type = serializer.validated_data.get('user_type')
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')

            users = User.objects.values_list('username', 'email')

            if users.filter(username__iexact=username):
                data = {'message':'Username already taken. We already have a registered user with this username. You can log in or if you forgot your password, you can click "Forgot password" button to reset your password'}
                return Response({'error':data,"success":False}, status=status.HTTP_400_BAD_REQUEST)        

            if users.filter(email__iexact=email):
                data = {'message':'Email already exists. We already have a registered user with this email address. You can log in or if you forgot your password, you can click "Forgot password" button to reset your password'}
                return Response({'error':data,"success":False}, status=status.HTTP_400_BAD_REQUEST)

            if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
                return Response({'error':{"message": "The password must contain at least 1 symbol: " + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"},"success":False}, status=status.HTTP_400_BAD_REQUEST)
            if not re.findall('[a-z]', password):
                return Response({'error':{"message": "The password must contain at least 1 lowercase letter, a-z."},"success":False}, status=status.HTTP_400_BAD_REQUEST)
            if not re.findall('[A-Z]', password):
                return Response({'error':{"message": "The password must contain at least 1 uppercase letter, A-Z."},"success":False}, status=status.HTTP_400_BAD_REQUEST)
            if not re.findall('\d', password): 
                return Response({'error':{"message": "The password must contain at least 1 digit, 0-9."},"success":False}, status=status.HTTP_400_BAD_REQUEST)
            else: 
                user = serializer.save()
                if user_type == 'Employer':
                    Employer.objects.create(user=user, description=description, title=title, country=country)
                elif user_type == 'Applicant':
                    Applicant.objects.create(user=user, description=description, title=title, country=country, interested_with=interested_with)
                elif user_type == 'Guest':
                    pass
            
                return Response({'message':'OK'}, status=status.HTTP_200_OK)

        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)



class ProfileAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)


            try:
                employer = Employer.objects.get(user=user)
            except ObjectDoesNotExist:
                employer = None

            try:
                applicant = Applicant.objects.get(user=user)
            except ObjectDoesNotExist:
                applicant = None

            if employer:
                pass
            elif applicant:
                user_serialized = UserSerializer(user).data
                return Response({'data':user_serialized}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'User doesn`t have profile!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
