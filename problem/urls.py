from django.urls import path
from .views import *
from .serializers import *
app_name = 'blog'

urlpatterns =[
    path('', ProblemCreateView.as_view(), name='problem-create'),
    path('levellist/<str:level>/', ProblemByLevelAPIViewlist.as_view(), name='api-problems-by-level'),
    path('chapterlist/<str:chapter>/', ProblemByChapterAPIViewlist.as_view(), name='api-problems-by-chapter'),
    path('userproblem/', UserProblemCreateView.as_view(), name='user-problem-create'),
    path('wrongproblems/', WrongProblemsAPIView.as_view(), name='wrong-problems'),
    path('yetproblems/', YetToSolveProblemsAPIView.as_view(), name='yet-to-solve-problems'),
    path('unsolved/chapter/<str:chapter>/', UnsolvedProblemsByChapterAPIView.as_view(), name='unsolved-problems-by-chapter'),
    path('reports/weekly/', WeeklyReportAPIView.as_view(), name='weekly-report'),
    
]