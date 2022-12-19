from accounts.models import Category
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Advertisement, AppliedJobs
from .serializers import AdvertisementSerializer, AppliedJobSerializer
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
