from django.urls import path
from .views import *
from .serializers import *
app_name = 'blog'

urlpatterns =[
    path('', ProblemCreateView.as_view(), name='problem-create'),
    path('level/<str:level>/', ProblemByLevelAPIView.as_view(), name='api-problems-by-level'),
    path('chapter/<str:chapter>/', ProblemByChapterAPIView.as_view(), name='api-problems-by-chapter'),
]