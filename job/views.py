from rest_framework import generics, permissions
from .models import JobListing
from .serializers import JobListingSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


# checking the permission for listing the job whether the user is admin or employer
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["Employer", "Admin"]


class JobListCreateView(generics.ListCreateAPIView):
    """
    View to list all job listings or create a new job listing.
    Methods:
    - get_queryset: Filters job listings based on user role. Employers can only see their job listings.
    - perform_create: Saves the job listing under the employer's company when creating a new listing.
    """

    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]

    def get_queryset(self):
        """
        Returns the queryset of job listings.Employers can only see their job listings, Admins can view all job listings.
        """
        if self.request.user.role == "Employer":
            return JobListing.objects.filter(company__owner=self.request.user)
        return JobListing.objects.all()

    def perform_create(self, serializer):
        """
        Handles the creation of a new job listing.If the user is an employer, the job listing is automatically associated with the employer's company.
        """
        if self.request.user.role in ["Admin", "Candidate"]:
            raise PermissionDenied("You cannot create job listing...")
        if self.request.user.role == "Employer":
            company = self.request.user.companies.first()
            serializer.save(company=company)


class JobListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    - Employers can only view, update, or delete their own job listings.
    - Admins can view or delete any job listing.
    Methods:
    - get_queryset: Filters job listings based on role
    """

    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]

    def get_queryset(self):
        if self.request.user.role == "Employer":
            return JobListing.objects.filter(company__owner=self.request.user)
        return JobListing.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Prevent admins and candidates from updating job listings,Only employers can update job listings of their own company jobs.
        """
        if self.request.user.role in ["Admin", "Candidate"]:
            raise PermissionDenied("You cannot update job listings.")
        if (
            request.user.role == "Employer"
            and job_listing.company.owner != request.user
        ):
            raise PermissionDenied(
                "You can only update job listings from your own company."
            )
        return super().update(request, *args, **kwargs)
