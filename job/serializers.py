from rest_framework import serializers
from .models import JobListing,JobApplication


class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = [
            "id",
            "title",
            "description",
            "requirements",
            "location",
            "salary",
            "is_active",
        ]

class JobApplication(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"