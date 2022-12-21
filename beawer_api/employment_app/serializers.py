from rest_framework import serializers
from .models import Advertisement, AppliedJobs
from accounts.serializers import EmployerSerializer, CategorySerializer

JOB_TYPES = [
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Intern', 'Intern'),
    ('Remote', 'Remote'),
    ('Hybrid', 'Hybrid'),
]

class AdvertisementSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    date_published = serializers.DateTimeField(format="%d.%m.%Y")
    class Meta:
        model = Advertisement
        fields = '__all__'


class AppliedJobSerializer(serializers.ModelSerializer):
    job = AdvertisementSerializer(many=False, read_only=True)
    applicant = serializers.StringRelatedField()
    applicated_date = serializers.DateTimeField(format="%d.%m.%Y")
    class Meta:
        model = AppliedJobs
        fields = '__all__'




class CreateAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        exclude = ['enabled', 'date_published']




class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJobs
        exclude = ['applicated_date', 'enabled', 'status']


class SearchJobSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    job_type = serializers.ChoiceField(required=False, choices=JOB_TYPES)