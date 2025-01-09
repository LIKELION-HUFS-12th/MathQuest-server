from django.urls import path
from .views import *
app_name = 'user'

urlpatterns = [
    path('delete/', delete, name='delete_account'),
    path('auth/username-check/', UsernameCheckView.as_view(), name='username_check'),
]
