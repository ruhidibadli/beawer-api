from accounts.models import Category
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Advertisement, AppliedJobs
from .serializers import AdvertisementSerializer, AppliedJobSerializer, CreateAdvertisementSerializer, ApplyJobSerializer
from accounts.serializers import CategorySerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class ReturnCategoriesAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        categories_serialized = CategorySerializer(categories, many=True).data


        return Response({'data':categories_serialized}, status=status.HTTP_200_OK)

class ReturnCategoryJobsAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, category_name):
        try:
            jobs = Advertisement.objects.filter(category__category_name=category_name, enabled=True)

            jobs_serialized = AdvertisementSerializer(jobs, many=True).data

            return Response({'data':jobs_serialized}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)




class ReturnAppliedJobsAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'error':'User not found!'}, status=status.HTTP_400_BAD_REQUEST)

        applied_jobs = AppliedJobs.objects.filter(applicant__user=user, enabled=True)

        applied_jobs_serialized = AppliedJobSerializer(applied_jobs, many=True).data

        return Response({'data':applied_jobs_serialized}, status=status.HTTP_200_OK)



class CreateAdvertisementAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateAdvertisementSerializer
    def post(self, request):
        serializer = CreateAdvertisementSerializer(data=request.data)

        if serializer.is_valid():
            try:
                employer = serializer.validated_data.get('employer')
                category = serializer.validated_data.get('category')
                title = serializer.validated_data.get('title')
                salary = serializer.validated_data.get('salary')
                job_type = serializer.validated_data.get('job_type')
                country = serializer.validated_data.get('country')

                created_job = Advertisement.objects.create(employer=employer, category=category, title=title, salary=salary, job_type=job_type, country=country)

                created_job_serialized = AdvertisementSerializer(created_job).data

                return Response({'data':created_job_serialized}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)



class ApplyJobAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ApplyJobSerializer

    def post(self, request):
        serializer =ApplyJobSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                applicant = serializer.validated_data.get('applicant')
                job = serializer.validated_data.get('job')
                job_status = serializer.validated_data.get('status')


                created_apply = AppliedJobs.objects.create(applicant=applicant, job=job, status=job_status)

                created_apply_serialized = AppliedJobSerializer(created_apply).data

                return Response({'data':created_apply_serialized}, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
            


