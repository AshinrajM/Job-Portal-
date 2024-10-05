from rest_framework import serializers
from .models import JobListing, JobApplication


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


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["job", "resume", "cover_letter","status"]

    def validate_resume(self, value):
        """
        Check that the uploaded resume is a PDF file.
        """
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are allowed for resumes.")
        return value

    def validate(self, attrs):
        """
        Check for duplicate applications by the same candidate for the same job.
        """
        print("Full Request Data:", self.context["request"].data)

        user = self.context["request"].user  # Get the logged-in user (candidate)
        job_id = attrs.get("job")  # Get the job ID from the input data

        # Check if the application already exists
        if JobApplication.objects.filter(candidate=user, job_id=job_id).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        return attrs
