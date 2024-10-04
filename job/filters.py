import django_filters
from .models import JobListing


class JobListingFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    company = django_filters.CharFilter(
        field_name="company__name", lookup_expr="icontains"
    )
    location = django_filters.CharFilter(lookup_expr="icontains")
    salary = django_filters.NumberFilter()
    min_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="gte")
    max_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="lte")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = JobListing
        fields = ["title", "company", "location", "salary", "is_active"]
