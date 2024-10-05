from .models import JobListing, JobApplication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobListingFilter
from rest_framework import filters
from rest_framework import generics, permissions, viewsets
from .serializers import JobListingSerializer, JobApplicationSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


# checking the permission for listing the job whether the user is admin or employer
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all users (including candidates) to view job listings
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ["Employer", "Admin"]


class JobListCreateView(generics.ListCreateAPIView):
    """
    View to list all job listings or create a new job listing.
    - get_queryset: Filters job listings based on user role. Employers can only see their job listings.
    - perform_create: Saves the job listing under the employer's company when creating a new listing.
    """

    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]
    # pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobListingFilter
    search_fields = ["title", "company__name", "location"]

    def get_queryset(self):
        """
        Returns the queryset of job listings.Employers can only see their job listings, Admins and Candidates can view all job listings.
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


class IsAdminOrEmployerOrCandidate(permissions.BasePermission):
    """
    - Admins: Full access to view, create, update, and delete.
    - Employers: Can view, update, and delete job applications for their job listings.
    - Candidates: Can create new job applications, and view their own applications.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.role == "Admin":
            return True

        # Employers can view, update, and delete applications for their own job listings
        if request.user.role == "Employer":
            return obj.job.company.owner == request.user

        # Candidates can only view or create their own applications
        if request.user.role == "Candidate":
            # Candidates can view their own applications
            if view.action in ["retrieve", "list"]:
                return obj.candidate == request.user
            # Candidates can create applications but not update or delete them
            return view.action == "create"

        # Default: No access for other roles
        return False


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    - Admins: Full access to all applications.
    - Employers: Can view applications for their job listings.
    - Candidates: Can view their own applications and apply to jobs.
    """

    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrEmployerOrCandidate,
    ]
    # pagination_class = None

    def get_queryset(self):
        user = self.request.user

        if user.role == "Admin":
            # Admins can see all job applications
            return JobApplication.objects.all()

        elif user.role == "Employer":
            # Employers can only see applications for their job listings
            return JobApplication.objects.filter(job__company__owner=user)

        elif user.role == "Candidate":
            # Candidates can see only their own job applications
            return JobApplication.objects.filter(candidate=user)

        # Default: No access for other roles
        return JobApplication.objects.none()

    def perform_create(self, serializer):
        """
        When a candidate applies to a job, attach the candidate to the application.
        """

        user = self.request.user
        if user.role == "Candidate":
            serializer.save(candidate=user)
        else:
            raise PermissionDenied("Only candidates can apply for jobs.")

    def perform_update(self, serializer):
        """
        Logic to allow only employers or admins to update job applications.
        Candidates cannot update their applications after submission.
        """
        user = self.request.user
        job_application = self.get_object()

        # Admins can update any job application
        if user.role == "Admin":
            serializer.save()

        # Employers can update applications for their job listings
        elif user.role == "Employer" and job_application.job.company.owner == user:
            serializer.save()

        else:
            raise PermissionDenied(
                "You do not have permission to update this application."
            )

    def perform_destroy(self, instance):
        """
        Logic for deleting job applications, allowing only admins and employers.
        """
        user = self.request.user
        if user.role == "Admin" or (
            user.role == "Employer" and instance.job.company.owner == user
        ):
            instance.delete()
        else:
            raise PermissionDenied(
                "You do not have permission to delete this application."
            )
