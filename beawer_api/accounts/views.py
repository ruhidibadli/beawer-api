from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Employer, Applicant, Category
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignUpSerializer, UserSerializer, EmailSerializer, EmployerSerializer, ApplicantSerializer, UpdateProfileSerializer
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
                    try:
                        applicant = Applicant.objects.get(user=user)
                        return Response({'data':{'user_id':user.id, 'user_type':'Applicant'}}, status=status.HTTP_200_OK)

                    except ObjectDoesNotExist:
                        pass

                    try:
                        employer = Employer.objects.get(user=user)
                        return Response({'data':{'user_id':user.id, 'user_type':'Employer'}}, status=status.HTTP_200_OK)

                    except ObjectDoesNotExist:
                        pass

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
            birth_date = serializer.validated_data.get('birth_date')
            email = serializer.validated_data.get('email').lower()
            username = serializer.validated_data.get('username').lower()
            full_name = serializer.validated_data.get('full_name')
            password = serializer.validated_data.get('password')
            interested_with = serializer.validated_data.get('interested_with')
            user_type = serializer.validated_data.get('user_type')
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            
            print(birth_date)
            users = User.objects.values_list('username', 'email')

            if users.filter(username__iexact=username):
                data = {'message':'Username already taken. We already have a registered user with this username. You can log in or if you forgot your password, you can click "Forgot password" button to reset your password'}
                return Response({'error':data,"success":False}, status=status.HTTP_400_BAD_REQUEST)        

            if users.filter(email__iexact=email):
                data = {'message':'Email already exists. We already have a registered user with this email address. You can log in or if you forgot your password, you can click "Forgot password" button to reset your password'}
                return Response({'error':data,"success":False}, status=status.HTTP_400_BAD_REQUEST)

            
            user = serializer.save()
            if user_type == 'Employer':
                Employer.objects.create(user=user, title=title, full_name=full_name, birth_date=birth_date)
            elif user_type == 'Applicant':
                created_applicant = Applicant.objects.create(user=user, description=description, title=title, full_name=full_name, birth_date=birth_date)
                print(interested_with)
                id_list = [t['id'] for t in interested_with]
                created_applicant.interested_with.set(id_list)
                created_applicant.save()
            elif user_type == 'Guest':
                pass
        
            return Response({'message':'OK'}, status=status.HTTP_200_OK)

        else:
            print(serializer.errors)
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)



class ProfileAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)


            try:
                employer = Employer.objects.get(user=user)
                employer_serialized = EmployerSerializer(employer).data

                return Response({'data':employer_serialized, 'email':user.email, 'user_type':'Employer'}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                employer = None

            try:
                applicant = Applicant.objects.get(user=user)
                applicant_serialized = ApplicantSerializer(applicant).data
                return Response({'data':applicant_serialized, 'email':user.email, 'user_type':'Applicant'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                applicant = None

            return Response({'error':'User doesn`t have profile!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)




class CheckEmailAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
                user_serialized = UserSerializer(user).data
                return Response({'data':user_serialized, 'error':None}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'data':None, 'error':'User with given email does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data':None, 'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)

    

class UpdateUserProfileAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, user_id):
        serializer = UpdateProfileSerializer(data=request.data)

        if serializer.is_valid():
            full_name = serializer.validated_data.get('full_name')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')

            try:
                user = User.objects.get(id=user_id)
            except ObjectDoesNotExist:
                return Response({'error':'User with given id not found!'}, status=status.HTTP_200_OK)

            applicant = user.applicant_set.get()
            
            user.username = username
            user.email = email
            applicant.title = title
            applicant.full_name = full_name
            applicant.description = description

            user.save()
            applicant.save()

            return Response({'data':'Ok'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_200_OK)