from django.urls import path
from . import views

urlpatterns = [
    path('get_categories/', views.ReturnCategoriesAPI.as_view(), name='get_categories'),
    path('get_category_jobs/<str:category_name>/', views.ReturnCategoryJobsAPI.as_view(), name='get_category_jobs'),
    path('get_applied_jobs/<int:user_id>/', views.ReturnAppliedJobsAPI.as_view(), name='get_applied_jobs'),
]