from rest_framework import serializers
from .models import Advertisement, AppliedJobs



class AdvertisementSerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    date_published = serializers.DateTimeField(format="%b, %d, %Y, %I:%M %p")
    class Meta:
        model = Advertisement
        fields = '__all__'


class AppliedJobSerializer(serializers.ModelSerializer):
    job = AdvertisementSerializer(many=False, read_only=True)
    applicant = serializers.StringRelatedField()
    applicated_date = serializers.DateTimeField(format="%b, %d, %Y, %I:%M %p")
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
        exclude = ['applicated_date', 'enabled']