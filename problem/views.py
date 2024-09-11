# problem/views.py
from rest_framework import generics
from .models import Problem
from .serializers import ProblemSerializer

# 문제 포스트하기
class ProblemCreateView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

# 학년에 따라 불러오기 (filter)
class ProblemByLevelAPIView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        level = self.kwargs['level'] 
        return Problem.objects.filter(level=level)

# 챕터에 따라 불러오기 (filter) 
class ProblemByChapterAPIView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        chapter = self.kwargs['chapter']
        return Problem.objects.filter(chapter=chapter)