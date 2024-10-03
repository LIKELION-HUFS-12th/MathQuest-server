from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout

def delete(request):
    request.user.delete()
    logout(request)
    return redirect('articles:index')