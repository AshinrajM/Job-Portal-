from .models import JobListing
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobListingFilter
from rest_framework import filters
from rest_framework import generics, permissions
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobListingFilter
    search_fields = ["title", "company__name", "location"]

    def get_queryset(self):
        """
        Returns the queryset of job listings.Employers can only see their job listings, Admins can view all job listings.
        """
        if self.request.user.role == "Employer":
            return JobListing.objects.filter(company__owner=self.request.user)
        return JobListing.objects.all()

    def perform_create(self, serializer):
        """
        Handles the creation of a new job listing.
        Ensures that the job is always associated with the logged-in employer's company.
        """

        user = self.request.user

        # Only Admins and Candidates cannot create job listings

        if user.role in ["Admin", "Candidate"]:
            raise PermissionDenied("You cannot create job listings.")

        # Employer job listing creation
        if user.role == "Employer":
            company = user.companies.first()

            if not company:
                raise ValidationError(
                    "You must have a company associated with your account to create job listings."
                )

            # Check if the request includes a company and whether it matches the employer's company
            request_company = self.request.data.get("company")

            if request_company and str(company.id) != request_company:
                raise PermissionDenied(
                    "You can only create job listings for your own company."
                )

            # Save the job listing with the employer's company, ignoring any provided company value
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
