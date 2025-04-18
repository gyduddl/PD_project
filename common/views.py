from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def logout_view(request):
    auth_logout(request)
    return redirect('polls:index')