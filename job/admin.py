from django.contrib import admin
from job.models import Company, JobListing, JobApplication

admin.site.register(Company)
admin.site.register(JobListing)
admin.site.register(JobApplication)
