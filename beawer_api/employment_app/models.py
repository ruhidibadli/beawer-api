from django.db import models
from accounts.models import Employer, Applicant, Category
from django.utils import timezone
# Create your models here.

JOB_TYPES = [
    ('FULL TIME', 'FULL TIME'),
    ('PART TIME', 'PART TIME'),
    ('INTERN', 'INTERN'),
    ('REMOTE', 'REMOTE'),
    ('HYBRID', 'HYBRID'),
]

APPLIEMENT_STATUS = [
    ('Waiting', 'Waiting'),
    ('Viewed', 'Viewed'),
    ('Interview Phase', 'Interview Phase'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected')

]

JOB_POSITIONS = [
    ('Junior', 'Junior'),
    ('Middle', 'Middle'),
    ('Senior', 'Senior'),
    ('Graduated', 'Graduated'),
    ('Experienced', 'Experienced'),
]


class Advertisement(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    salary = models.IntegerField()
    job_type = models.CharField(choices=JOB_TYPES, max_length=50)
    country = models.CharField(max_length=255)
    date_published = models.DateTimeField(default=timezone.now)
    enabled = models.BooleanField(default=True)
    position = models.CharField(max_length=50, choices=JOB_POSITIONS, default='Junior')
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class AppliedJobs(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    applicated_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=APPLIEMENT_STATUS, max_length=25, default='Waiting')
    enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.applicant.user.username} - {self.job.title}'
