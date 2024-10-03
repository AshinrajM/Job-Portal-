from rest_framework import generics, permissions
from .models import JobListing
from .serializers import JobListingSerializer
from rest_framework.permissions import IsAuthenticated


#checking the permission for listing the job whether the user is admin or employer
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['Employer', 'Admin'] 


class JobListCreateView(generics.ListCreateAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]


    def get_queryset(self):
        # Employers can only see their job listings
        if self.request.user.role == 'Employer':
            return JobListing.objects.filter(comapny__owner=self.request.user)
        return JobListing.objects.all()


    def perform_create(self,serializer):
        if self.request.user.role == 'Employer':
            company = self.request.user.companies.first()
            serializer.save(comapny=company)


class JobListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]

    def get_queryset(self):
        # Employers can only see their job listings
        if self.request.user.role == 'Employer':
            return JobListing.objects.filter(comapny__owner=self.request.user)
        return JobListing.objects.all()