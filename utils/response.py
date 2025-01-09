from rest_framework.response import Response

def custom_response(code, msg, data=None, status_code=200):
   
    return Response({
        "code": code,
        "msg": msg,
        "data": data
    }, status=code)
