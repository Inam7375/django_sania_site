from django.db import connections
from django.db import models
# Create your models here.

class Student(models.Model):
    s_id = models.IntegerField(primary_key=True, auto_created=True, serialize=False)
    s_name = models.CharField(max_length=100)
    s_dept = models.CharField(max_length=100)
    s_password = models.CharField(max_length=100)
    s_semester = models.IntegerField()
    s_section = models.CharField(max_length=100)
    s_email = models.CharField(max_length=100)
    s_Fathername = models.CharField(max_length=100)
    s_gender = models.CharField(max_length=20)
    s_phoneno = models.CharField(max_length=20)
    class Meta:
        db_table = "student"

class Admin(models.Model):
    A_id = models.IntegerField(primary_key=True, auto_created=True, serialize=False)
    A_name = models.CharField(max_length=100)
    A_AcademicYear = models.IntegerField()
    A_gender = models.CharField(max_length=20)
    A_qualification = models.CharField(max_length=100)
    A_phoneNo = models.IntegerField()
    A_designation = models.CharField(max_length=100)
    A_email = models.CharField(max_length=100)
    A_password = models.CharField(max_length=100)
    class Meta:
        db_table = "admin"

class Teacher(models.Model):
    t_id = models.IntegerField(primary_key=True)
    t_name = models.CharField(max_length=100)
    t_dept = models.CharField(max_length=100)
    t_email = models.CharField(max_length=100)
    t_phoneno = models.CharField(max_length=20)
    t_gender = models.CharField(max_length=20)
    # t_qaulification = models.CharField(max_length=100)
    t_designation = models.CharField(max_length=50)
    t_password = models.CharField(max_length=50)
    class Meta: 
        db_table = "teacher"

class Userreg(models.Model):
    uname = models.CharField(max_length=100)
    uemail = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    repwd = models.CharField(max_length=100)
    class Meta:
        db_table = "newuserreg"

class Attendance(models.Model):
    sc_id = models.IntegerField()
    Atten_Status = models.CharField(max_length=50)
    Atten_datetime = models.DateTimeField()
    class Meta:
        db_table = "attendance"

class StdCourse(models.Model):
    SC_id = models.IntegerField()
    c_id = models.IntegerField()
    S_id = models.IntegerField()
    class Meta:
        db_table = "stdCourse"

class Course(models.Model):
    C_id = models.IntegerField()
    C_name = models.CharField(max_length=50)
    C_sessionstart = models.IntegerField()
    C_sessionend = models.IntegerField()
    T_id = models.IntegerField()
    class Meta:
        db_table = "course"