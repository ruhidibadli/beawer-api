from rest_framework import serializers
from .models import Advertisement, AppliedJobs



class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fileds = '__all__'


class AppliedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedJobs
        fields = '__all__'