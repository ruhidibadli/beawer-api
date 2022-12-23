from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('signup/', views.SignUpAPI.as_view(), name='signup'),
    path('profile/<int:user_id>/', views.ProfileAPI.as_view(), name='profile'),
    path('check_email/', views.CheckEmailAPI.as_view(), name='check_email'),
    path('update_profile/<int:user_id>/', views.UpdateUserProfileAPI.as_view(), name='update_profile'),
]


