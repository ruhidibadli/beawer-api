from django.urls import path
from . import views

urlpatterns = [
    path('get_categories/', views.ReturnCategoriesAPI.as_view(), name='get_categories'),
    path('get_category_jobs/<int:category_id>/', views.ReturnCategoryJobsAPI.as_view(), name='get_category_jobs'),
    path('get_applied_jobs/<int:user_id>/', views.ReturnAppliedJobsAPI.as_view(), name='get_applied_jobs'),
    path('create_job/', views.CreateAdvertisementAPI.as_view(), name='create_job'),
    path('apply_job/', views.ApplyJobAPI.as_view(), name='apply_job'),
    path('job_detail/<int:job_id>/', views.JobDetailAPI.as_view(), name='job_detail'),
    path('my_jobs/<int:user_id>/', views.ShowMyJobsAPI.as_view(), name='my_jobs'),
    path('update_job/<int:pk>/', views.UpdateJobAPI.as_view(), name='update_job'),
]