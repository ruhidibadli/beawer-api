from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category_name

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='static/img/')
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interested_with = models.ManyToManyField(Category, null=True, blank=True)
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to='static/img/')
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username