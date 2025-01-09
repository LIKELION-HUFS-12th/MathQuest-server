
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["DELETE"])
def delete(request):
    if request.user.is_authenticated:  # 로그인 상태 확인
        request.user.delete()  # 사용자 삭제
        logout(request)  # 세션 로그아웃
        return JsonResponse({'message': '회원 탈퇴가 완료되었습니다.'}, status=204)
    else:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=403)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.response import custom_response
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameCheckView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        # 유효성 검사
        if not username:
            return custom_response(
                code=400,
                msg="아이디를 입력해주세요.",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # 아이디 중복 체크
        if User.objects.filter(username=username).exists():
            return custom_response(
                code=409,
                msg="이미 사용중인 아이디 입니다다.",
                data={"is_available": False},
                status_code=status.HTTP_409_CONFLICT
            )

        # 사용 가능한 아이디
        return custom_response(
            code=200,
            msg="사용 가능한 아이디 입니다다.",
            data={"is_available": True},
            status_code=status.HTTP_200_OK
        )


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                code=200,
                msg="회원 정보가 성공적으로 수정되었습니다.",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        
        return custom_response(
            code=400,
            msg="회원 정보 수정 중 오류가 발생했습니다.",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
