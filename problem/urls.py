from django.urls import path
from .views import *
app_name = 'problem'
urlpatterns = [
    path('create/', ProblemCreateView.as_view(), name='problem_create'),
    path('bulk-create/', BulkProblemCreateView.as_view(), name='bulk_problem_create'),
    path('levellist/<str:level>/', ProblemByLevelAPIViewlist.as_view(), name='problem_by_level'),
    path('chapterlist/<str:chapter>/', ProblemByChapterAPIViewlist.as_view(), name='problem_by_chapter'),
    path('learning-options/', LearningOptionsView.as_view(), name='learning_options'),
    path('userproblem/', UserProblemStatusUpdateView.as_view(), name='user_problem_status_update'),
    path('wrongproblems/', WrongProblemsAPIView.as_view(), name='wrong-problems'),
    path('wrong-notes/chapter/<str:chapter>/', WrongNotesByChapterView.as_view(), name='wrong_notes_by_chapter'),
    path('reports/weekly/', WeeklyReportView.as_view(), name='weekly_report'),
    path('chapter_difficulty/<str:level>/<str:difficulty>/', ProblemsByChapterAndDifficultyAPIView.as_view(), name='problems_by_chapter_difficulty'),
    path('attendance/<int:year>/<int:month>/', MonthlyAttendanceView.as_view(), name='monthly_attendance'),
]

