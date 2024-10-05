from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobListCreateView,
    JobListDetailView,
    JobApplicationViewSet,
    CompanyUpdateView,
)


router = DefaultRouter()
router.register(r"job-applications", JobApplicationViewSet, basename="jobapplication")

urlpatterns = [
    path(
        "company/<int:pk>/update/", CompanyUpdateView.as_view(), name="company_update"
    ),
    path("job-list/", JobListCreateView.as_view(), name="job_list_create"),
    path("job-list/<int:pk>/", JobListDetailView.as_view(), name="job_list_detail"),
    path("", include(router.urls)),
]
