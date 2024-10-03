from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

def delete(request):
    print(request.user)  # 사용자 상태 출력
    if request.user.is_authenticated:  # 사용자가 로그인 상태인지 확인
        request.user.delete()  # 사용자 삭제
        logout(request)  # 로그아웃 처리
        return JsonResponse({'message': '회원 탈퇴가 완료되었습니다.'}, status=204)
    else:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=403)  # 로그인 안된 경우 에러 메시지
