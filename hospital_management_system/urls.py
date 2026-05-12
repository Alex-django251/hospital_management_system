"""
URL configuration for hospital_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
#from users.views import run_migrations
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect('/api-auth/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home), 
    path('api/doctor/', include('doctors.urls')),
    path('api/patient/', include('patients.urls')),
    
    path('', include('dashboards.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/', include('users.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('', include('billing.urls')),
    path('api/labreports/', include('labreports.urls')),
    path('api/receptionist/', include('receptionist.urls')),
    
    path('api-auth/', include('rest_framework.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
   # path('run-migrations/', run_migrations),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
