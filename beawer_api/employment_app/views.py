from accounts.models import Category
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Advertisement, AppliedJobs
from .serializers import AdvertisementSerializer, AppliedJobSerializer, CreateAdvertisementSerializer, ApplyJobSerializer, SearchJobSerializer
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
    
    def get(self, request, category_id):
        try:
            jobs = Advertisement.objects.filter(category__id=category_id, enabled=True)

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

        applied_jobs_serialized = []
        temp = 0
        for job in applied_jobs:
            applied_jobs_serialized.append(AppliedJobSerializer(job).data)
            try:
                applied_jobs_serialized[temp].update({'job_image':job.job.employer.image.url})
            except:
                pass
            temp += 1
        # applied_jobs_serialized = AppliedJobSerializer(applied_jobs, many=True).data

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
                position = serializer.validated_data.get('position')
                description = serializer.validated_data.get('description')

                created_job = Advertisement.objects.create(employer=employer, category=category, title=title, salary=salary, job_type=job_type, country=country, position=position, description=description)

                created_job_serialized = AdvertisementSerializer(created_job).data

                return Response({'data':created_job_serialized, 'company_image':created_job.employer.image.url}, status=status.HTTP_200_OK)
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


                created_apply = AppliedJobs.objects.create(applicant=applicant, job=job)

                created_apply_serialized = AppliedJobSerializer(created_apply).data

                return Response({'data':created_apply_serialized, 'job_image':created_apply.job.employer.image.url}, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
            



class JobDetailAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, job_id):
        try:
            job = Advertisement.objects.get(id=job_id)

            job_serialized = AdvertisementSerializer(job).data

            return Response({'data':job_serialized, 'company_image':job.employer.image.url}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)




class ShowMyJobsAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        try:
            my_jobs = Advertisement.objects.filter(enabled=True, employer__user__id=user_id)
            my_jobs_serialized = AdvertisementSerializer(my_jobs, many=True).data

            return Response({'data':my_jobs_serialized}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


    
class UpdateJobAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateAdvertisementSerializer
    def put(self, request, pk):
        try:
            job = Advertisement.objects.get(id=pk)
            serializer = CreateAdvertisementSerializer(job, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            job = Advertisement.objects.get(id=pk)
            job.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)




class SearchJobsAPI(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchJobSerializer

    def post(self, request):
        serializer = SearchJobSerializer(data=request.data)

        if serializer.is_valid():
            category_id = serializer.validated_data.get('category_id')
            job_type = serializer.validated_data.get('job_type')

            jobs = Advertisement.objects.filter(category__id=category_id, job_type=job_type)

            jobs_serialized = AdvertisementSerializer(jobs, many=True).data

            return Response({'data':jobs_serialized}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Data is not valid!'}, status=status.HTTP_400_BAD_REQUEST)