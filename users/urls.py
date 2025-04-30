from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.UserCreateView.as_view(), name='create')
]
