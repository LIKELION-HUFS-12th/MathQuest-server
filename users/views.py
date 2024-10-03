from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

@require_POST  # POST 요청만 허용
def delete(request):
    request.user.delete()  # 사용자 삭제
    logout(request)  # 로그아웃 처리
    return JsonResponse({'message': '회원 탈퇴가 완료되었습니다.'}, status=204)