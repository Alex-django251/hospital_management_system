from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'doctor':
                return redirect('/api/doctor/dashboard/')
            elif user.role == 'patient':
                return redirect('/api/patient/dashboard/')
            elif user.role == 'receptionist':
                return redirect('/api/receptionist/dashboard/')
            else:
                return redirect('/admin/')
        return redirect('/api-auth/login/')



def after_login_redirect(user):
    if user.role == "doctor":
        return "/api/doctor/dashboard/"
    elif user.role == "patient":
        return "/api/patient/dashboard/"
    elif user.role == "receptionist":
        return "/api/receptionist/dashboard/"
    
    