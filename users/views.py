from django.shortcuts import render

def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles;index')