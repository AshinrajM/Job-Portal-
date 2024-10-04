from rest_framework import serializers
from .models import JobListing

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = ['title', 'description', 'requirements', 'location', 'salary', 'is_active']