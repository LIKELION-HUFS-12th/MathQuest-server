from django.urls import path
from . import views

app_name = 'users'

urlpatterns =[
    path('delete/', views.delete, name='delete'),
    
]