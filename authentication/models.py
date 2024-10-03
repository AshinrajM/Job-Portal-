from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('Candidate', 'Candidate'),
        ('Employer', 'Employer'),
        ('Admin', 'Admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Admin')

    def __str__(self):
        return self.username


