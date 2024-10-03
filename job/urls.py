from django.urls import path
from .views import JobListCreateView, JobListDetailView


urlpatterns = [
    path("job-list-create/", JobListCreateView.as_view(), name="job_list_create"),
    path("job-list/<int:pk>/", JobListDetailView.as_view(), name="job_list_detail"),
]
