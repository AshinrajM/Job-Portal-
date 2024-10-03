from django.db import models
from django.conf import settings


class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "Employer"},
        related_name="companies",
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class JobListing(models.Model):
    title = models.CharField(max_length=200)
    comapny = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='job_listings')
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

        