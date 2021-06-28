
# urls.py
"""textutils URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('forget.html', views.forget, name='forget'),
    path('reset.html', views.reset, name='reset'),
    path('A-Adminlogin.html', views.Adminlogin, name='A-Adminlogin'),
    path('A-dashboard.html', views.dashboard, name='A-dashboard'),
    path('A-Admindashboard.html', views.Admindashboard, name='A-Admindashboard'),
    path('A-Addstudent.html', views.Addstudent, name='A-Addstudent'),
    path('A-Addteacher.html', views.Addteacher, name='A-Addteacher'),
    path('A-initialreport.html', views.initialreport, name='A-initialreport'),
    path('A-massreport.html', views.massreport, name='A-massreport'),
    path('A-massreport1.html', views.massreport1, name='A-massreport1'),
    path('T-teacherlogin.html', views.teacherlogin, name='T-teacherlogin'),
    path('T-dashboard.html', views.Tdashboard, name='T-dashboard'),
    path('T-teacherdashboard.html', views.teacherdashboard, name='T-Teacherdashboard'),
    path('T-attendance.html', views.Tattendance, name='T-attendance'),
    path('T-studentreport.html', views.Tstudentreport, name='T-studentreport'),
    path('S-Studentlogin.html', views.Studentlogin, name='S-Studentlogin'),
    path('S-dashboard.html',views.S_dashboard,name='S-dashboard'),
    path('S-Studentdashboard.html', views.Sdashboard, name='S-Studentdashboard'),
    path('S-studentreport.html', views.studentreport, name='S-studentreport')
]