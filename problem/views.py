
from .models import Problem
from .serializers import ProblemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from  utils.response import custom_response
from rest_framework.permissions import IsAuthenticated
from .models import UserProblem, Problem, DailyScore, Attendance
from django.utils import timezone
from calendar import monthrange

class ProblemCreateView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

#여러 문제 한번에 추가, 리스트 형식
class BulkProblemCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProblemSerializer(data=request.data, many=True)  # many=True를 추가
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
# 학년에 따라 문제 불러오기
class ProblemByLevelAPIViewlist(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        level = self.kwargs['level']
        return Problem.objects.filter(level=level)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(
                code=200,
                msg="Success",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return custom_response(
            code=404,
            msg="해당 학년의 문제가 존제하지 않습니니다.",
            data=[],
            status_code=status.HTTP_404_NOT_FOUND
        )

# 챕터에 따라 문제 불러오기
class ProblemByChapterAPIViewlist(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        chapter = self.kwargs['chapter']
        return Problem.objects.filter(chapter=chapter)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(
                code=200,
                msg="Success",
                data=serializer.data
            )
        return custom_response(
            code=404,
            msg="해당 과목의 문제가 존재하지 않습니다.",
            data=[]
        )
    
class LearningOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # 로그인한 사용자 정보 가져오기
        current_school = user.school  # 예: "초등학교"

        # 학습 가능한 학년 목록 생성
        available_options = []

        if current_school == "초등학교":
            available_options = [
                f"초등학교 {i}학년" for i in range(3, 7)
            ]
        elif current_school == "중학교":
            available_options = [
                f"중학교 {i}학년" for i in range(1, 4)
            ]
        elif current_school == "고등학교":
            available_options = [
                f"고등학교 {i}학년" for i in range(1, 4)
            ]

        # 응답 데이터 반환
        return custom_response(
            code=200,
            msg="Success",
            data={
                "current_school": current_school,
                "available_options": available_options
            },
            status_code=200
        )
    from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import custom_response
from .models import UserProblem, Problem, DailyScore
from django.utils import timezone

class UserProblemStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  # 로그인한 사용자
        problem_id = request.data.get('problem_id')
        user_status = request.data.get('status')  # 'RIGHT', 'WRONG', 'YET'

        # 유효성 검사
        if user_status not in ['RIGHT', 'WRONG', 'YET']:
            return custom_response(
                code=400,
                msg="입력된 상태 값이 잘못되었습니다.",
                data=None
            )

        try:
            # 문제 가져오기
            problem = Problem.objects.get(id=problem_id)

            # UserProblem 업데이트 또는 생성
            user_problem, created = UserProblem.objects.update_or_create(
                user=user,
                problem=problem,
                defaults={'status': user_status}
            )

            # DailyScore 업데이트
            today = now().date()
            daily_score, _ = DailyScore.objects.get_or_create(user=user, date=today)

            if user_status == 'RIGHT':
                daily_score.correct_answers += 1
            elif user_status == 'WRONG':
                daily_score.incorrect_answers += 1

            daily_score.save()

            # **출석 체크 로직 추가**
            # 오늘 날짜에 출석 기록이 없으면 생성
            Attendance.objects.get_or_create(user=user, date=today)

            # 응답 반환
            return custom_response(
                code=200,
                msg="문제 상태가 정상적으로 변경되었고, 출석이 체크되었습니다.",
                data={
                    "problem_id": problem_id,
                    "status": user_status
                },
                status_code=200
            )

        except Problem.DoesNotExist:
            return custom_response(
                code=404,
                msg="해당 아이디의 문제가 없습니다.",
                data=None
            )
    
class WrongProblemsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # 오답 문제 필터링
        wrong_problems = Problem.objects.filter(
            userproblem__user=user,
            userproblem__status='WRONG'
        )

        if wrong_problems.exists():
            serializer = ProblemSerializer(wrong_problems, many=True)
            return custom_response(
                code=200,
                msg="오답 문제가 성공적으로 조회되었습니다.",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )

        # 오답 문제가 없을 경우
        return custom_response(
            code=404,
            msg="오답 문제가 없습니다.",
            data=[],
            status_code=status.HTTP_404_NOT_FOUND
        )
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import custom_response
from .models import UserProblem, Problem
from .serializers import ProblemSerializer

class WrongNotesByChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chapter, *args, **kwargs):
        user = request.user

        # 특정 챕터의 문제 가져오기
        user_problems = UserProblem.objects.filter(
            user=user,
            status="WRONG",
            problem__chapter=chapter  
        ).select_related('problem')  # problem 테이블 조인

    
        problems = [user_problem.problem for user_problem in user_problems]
        serializer = ProblemSerializer(problems, many=True)

        # 응답 반환
        if problems:
            return custom_response(
                code=200,
                msg="성공적으로 챕터별 틀린문제를 불러왔습니다.",
                data=serializer.data,
                status_code=200
            )
        else:
            return custom_response(
                code=404,
                msg="해당 챕터의 틀린문제가 없습니다.",
                data=[],
                status_code=404
            )

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.response import custom_response
from .models import DailyScore
from django.utils.timezone import now, timedelta

class WeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인한 사용자

        # 이번 주의 시작과 끝 날짜 계산
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # 월요일
        end_of_week = start_of_week + timedelta(days=6)  # 일요일

        # 주간 DailyScore 데이터를 가져오기
        weekly_scores = DailyScore.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        )

        # 초기화된 결과 딕셔너리 (월화수목금토일)
        correct = {str(i): 0 for i in range(7)}
        incorrect = {str(i): 0 for i in range(7)}

        # 주간 데이터 집계
        for score in weekly_scores:
            weekday = score.date.weekday()  # 0: 월요일, ..., 6: 일요일
            correct[str(weekday)] += score.correct_answers
            incorrect[str(weekday)] += score.incorrect_answers

        # 응답 반환
        return custom_response(
            code=200,
            msg="Weekly report fetched successfully.",
            data={
                "correct": correct,
                "incorrect": incorrect
            },
            status_code=200
        )

class ProblemsByChapterAndDifficultyAPIView(APIView):
    """
    특정 챕터와 난이도에 해당하는 문제를 필터링하는 뷰
    """
    def get(self, request, level, difficulty, *args, **kwargs):
        # 문제 필터링
        problems = Problem.objects.filter(level=level, difficulty=difficulty)

        if problems.exists():
            serializer = ProblemSerializer(problems, many=True)
            return custom_response(
                code=200,
                msg="Success",
                data=serializer.data
            )

        return custom_response(
            code=404,
            msg="해당 챕터와 난이도에 해당하는 문제가 없습니다.",
            data=[]
        )
    
from datetime import date, timedelta
from django.utils.timezone import now

class MonthlyAttendanceView(APIView):
    """
    한 달 동안의 출석 정보를 반환하는 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month, *args, **kwargs):
        user = request.user

        # 한 달의 시작 날짜와 마지막 날짜 계산
        start_date = date(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = date(year, month, last_day)

        # 해당 월의 출석 기록 조회
        attendance_records = Attendance.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).values_list('date', flat=True)

        # 출석 날짜를 집합으로 저장
        attendance_dates = {record for record in attendance_records}

        # 한 달 동안의 날짜별 출석 상태 생성
        monthly_attendance = []
        for day in range(1, last_day + 1):
            current_date = date(year, month, day)
            monthly_attendance.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "attended": current_date in attendance_dates
            })

        # 응답 반환
        return custom_response(
            code=200,
            msg="출석 기록 조회 성공",
            data={
                "year": year,
                "month": month,
                "attendance": monthly_attendance
            }
        )