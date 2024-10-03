# problem/views.py
from rest_framework import generics
from rest_framework import status
from .models import Problem, UserProblem
from .serializers import ProblemSerializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

# 문제 포스트하기
class ProblemCreateView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

# 학년에 따라 불러오기 (filter)
class ProblemByLevelAPIViewlist(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        level = self.kwargs['level'] 
        return Problem.objects.filter(level=level)

# 챕터에 따라 불러오기 (filter) 
class ProblemByChapterAPIViewlist(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        chapter = self.kwargs['chapter']
        return Problem.objects.filter(chapter=chapter)

# 문제 푼 상태로 변경
class UserProblemCreateView(generics.CreateAPIView):
    queryset = UserProblem.objects.all()
    serializer_class = ProblemSerializer

    def post(self, request, *args, **kwargs):
        user = request.user  # 현재 사용자
        problem_id = request.data.get('problem_id')
        user_status = request.data.get('status')

        try:
            problem = Problem.objects.get(id=problem_id)
            user_problem, created = UserProblem.objects.update_or_create(
                user=user,
                problem=problem,
                defaults={'status': user_status},
                
            )
            return Response({"message": "상태 업데이트 성공"}, status=status.HTTP_200_OK)
        except Problem.DoesNotExist:
            return Response({"error": "문제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
# 오답노트 기능
class WrongProblemsAPIView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        user = self.request.user
        return Problem.objects.filter(userproblem__user=user, userproblem__status='WRONG')

# 아직 안 푼 문제 필터링
class YetToSolveProblemsAPIView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        user = self.request.user
        return Problem.objects.filter(userproblem__user=user, userproblem__status='YET')

# 챕터 별 안 푼 문제 필터링
class UnsolvedProblemsByChapterAPIView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        user = self.request.user  # 현재 사용자
        chapter = self.kwargs['chapter']  # URL에서 챕터를 가져옴
        
        # 해당 챕터의 문제 중 사용자가 아직 풀지 않은 문제를 필터링
        return Problem.objects.filter(
            chapter=chapter
        ).exclude(
            userproblem__user=user
        )