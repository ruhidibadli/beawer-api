from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Employer)
admin.site.register(Applicant)
admin.site.register(Category)