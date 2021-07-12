
# views.py
# I have created this file
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from home.models import Attendance, Userreg
from django.contrib import messages
from django.db import connection
from home.models import Student, Teacher, Attendance, StdCourse, Course, Admin
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from json import dumps

user_role = ""
user_name = ""

def index(request):
    global user_role
    if user_role == "admin":
        return redirect('A-dashboard')
    return render(request, 'htmlFile/index.html')
    # return HttpResponse("Home")


def forget(request):
    return render(request, 'htmlFile/forget.html')

def reset(request):
    return render(request, 'htmlFile/reset.html')

def Adminlogin(request):
    global user_role
    global user_name
    if user_role == "":
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("pass")
            try:
                cursor = connection.cursor()
                cursor.execute(f'''
                    select A_name, A_id from admin where A_name = "{username}" and A_password="{password}"
                ''')
                user = cursor.fetchone()
                if user:
                    uname = user[0]
                    user_name = user[0]
                    user_role = 'admin'
                    return redirect('A-dashboard')            
                else:
                    print("Not found")
            except Exception as e:
                print(e)
        return render(request, 'htmlFile/A-Adminlogin.html')
    elif user_role=='admin':
        return redirect('A-dashboard')
    return redirect('index')

def dashboard(request):
    global user_role
    global user_name
    cursor = connection.cursor()
    cursor.execute(f'''
    select s_name from student
    ''')
    students = []
    stds = cursor.fetchall()
    stds = list(stds)
    for std in stds:
        std = str(std)
        std = std.strip("(")
        std = std.strip(")")
        std = std.strip(',')
        std = std.strip("'")
        students.append(std)
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            return redirect('index')
        if request.method == 'POST':
            date = request.POST.get("date")
            std = request.POST.get("st_name")
            if date and std:
                year, month = date.split('-')
                """
                Fetching monthly data
                """
                cursor = connection.cursor()
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="present" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                present = len(results)
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="absent" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                absent = len(results)

                """
                Fetching yearly data
                """
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="present" and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                ypresent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in ypresent:
                        ypresent[mon] = 1
                    else:
                        ypresent[mon] = ypresent[mon] + 1
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="absent" and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                yabsent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in yabsent:
                        yabsent[mon] = 1
                    else:
                        yabsent[mon] = yabsent[mon] + 1
                
                def Union(lst1, lst2):
                    final_list = list(set(lst1) | set(lst2))
                    return final_list
                pkeys = list(ypresent.keys())
                akeys = list(yabsent.keys())
                keys = Union(pkeys, akeys)
            return render(request, 'htmlFile/A-dashboard.html', {'uname':user_name, 'present':present, 'absent':absent, 'ypresent': json.dumps(ypresent), 'yabsent': json.dumps(yabsent), 'keys':json.dumps(keys), 'date':date, 'stdnts':students})
        return render(request, 'htmlFile/A-dashboard.html', {'uname':user_name, 'present':11, 'absent':12, 'ypresent': json.dumps({
            'june' : 15,
            'may' : 12
        }), 'yabsent': json.dumps({
            'june' : 15,
            'may' : 18
        }), 'keys':json.dumps(['june', 'may']), 'stdnts':students})
    return redirect('index')

def Admindashboard(request):
    global user_role
    global user_name
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            return redirect('index')
        cursor = connection.cursor()
        cursor.execute(f'''
            select * from admin where A_name = "{user_name}"
        ''')
        result = cursor.fetchone()
        if result:
            user_details = {}
            user_details['name'] = result[1]
            user_details['acyear'] = result[2]
            user_details['gender'] = result[3]
            user_details['qual'] = result[4]
            user_details['cell_no'] = result[5]
            user_details['email'] = result[6]
        return render(request, 'htmlFile/A-Admindashboard.html', {'uname': user_name, 'user':user_details})
    return redirect('index')

def Addstudent(request):
    global user_role
    global user_name
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == "POST":
            s_id = request.POST.get("st_id")
            try:
                if s_id:
                    student = Student.objects.get(s_id=s_id)
                    if student:
                        return render(request, 'htmlFile/A-Addstudent.html', {'msg': 'User already exists'})
                else:    
                    return render(request, 'htmlFile/A-Addstudent.html', {'msg': 'Fill in all the fields'})
            except:
                s_id = int(request.POST.get("st_id"))
                name = request.POST.get("st_name","")
                department = request.POST.get("st_dept","")
                semester = request.POST.get("st_sem","")
                section = request.POST.get("st_sec","")
                email = request.POST.get("st_email","")
                password = request.POST.get("st_pass","")
                fname = request.POST.get("st_fname","")
                gender = request.POST.get("gender","")
                phoneno = request.POST.get("st_num","")
                try:
                    student = Student(s_id = s_id, s_name = name, s_dept = department, s_semester = semester, s_section = section, s_email = email, s_password=password,s_Fathername=fname, s_gender=gender, s_phoneno=phoneno)
                    student.save();
                    return redirect("A-dashboard")
                except:
                    return render(request, 'htmlFile/A-Addstudent.html', {'msg': 'Fill in all the fields'})
        # else:
        #     return render(request, 'htmlFile/A-Addstudent.html', {'msg': 'Fill in all the fields'})
        return render(request, 'htmlFile/A-Addstudent.html', {'uname': user_name})
    return redirect('index')

def Addteacher(request):
    global user_role
    global user_name
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == "POST":
            tc_id = request.POST.get("tc_id")
            try:
                if tc_id:
                    teacher = Teacher.objects.get(t_id=tc_id)
                    if teacher:
                        return render(request, 'htmlFile/A-Addteacher.html', {'msg': 'User already exists', 'uname': user_name})
                else:    
                    return render(request, 'htmlFile/A-Addteacher.html', {'msg': 'Fill in all the fields', 'uname': user_name})
            except:
                tc_id = int(request.POST.get("tc_id"))
                name = request.POST.get("tc_name","")
                # qualification = request.POST.get("tc_qualf","")
                designation = request.POST.get("tc_design","")
                password = request.POST.get("tc_password","")
                print(password)
                department = request.POST.get("tc_dept","")
                email = request.POST.get("tc_email","")
                gender = request.POST.get("gender","")
                phoneno = request.POST.get("tc_num","")
                try:
                    teacher = Teacher(t_id = tc_id, t_name = name, t_dept = department, t_email=email, t_gender=gender, t_designation=designation, t_phoneno=phoneno, t_password=password)
                    teacher.save();
                    print("Saved")
                    return redirect("A-dashboard")
                except Exception as e:
                    print(e)
                    return render(request, 'htmlFile/A-Addteacher.html', {'msg': 'Fill in all the fields', 'uname':user_name})

        return render(request, 'htmlFile/A-Addteacher.html', {'uname': user_name})
    return redirect('index')

def initialreport(request):
    global user_role
    global user_name
    cursor = connection.cursor()
    cursor.execute(f'''
    select s_name from student
    ''')
    students = []
    stds = cursor.fetchall()
    stds = list(stds)
    for std in stds:
        std = str(std)
        std = std.strip("(")
        std = std.strip(")")
        std = std.strip(',')
        std = std.strip("'")
        students.append(std)
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            st_name = request.POST.get("st_name")
            print(st_name)
            course = request.POST.get("whichcourse")
            try:
                if st_name and course:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    cursor.execute(f'''
                    select studentcourse.s_id,student.s_name,student.s_dept, student.s_email, student.s_semester, student.s_section, course.C_name,Attendance.Atten_Status,Attendance.Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{st_name}" and C_name= "{course}";
                    ''')
                    results = cursor.fetchall()
                    result = {}
                    if len(results) > 0:
                        print("Yes man")
                        result['s_id'] = results[0][0]
                        result['s_name'] = results[0][1]
                        result['s_dept'] = results[0][2]
                        result['s_email'] = results[0][3]
                        result['s_semester'] = results[0][4]
                        result['s_section'] = results[0][5]
                        result['s_totalCLasses'] = len(results)
                        result['s_presentClassses'] = 0
                        result['s_absentClassses'] = 0
                        for r in results:
                            if r[7] == 'present':
                                result['s_presentClassses'] = result['s_presentClassses'] + 1
                            elif r[7] == 'absent':
                                result['s_absentClassses'] = result['s_absentClassses'] + 1
                        return render(request, 'htmlFile/A-initialreport.html', {'student': result, 'uname':user_name, 'stdnts': students})
                    return render(request, 'htmlFile/A-initialreport.html', {'msg': "No record found", 'uname':user_name, 'stdnts': students})
                else:    
                    return render(request, 'htmlFile/A-initialreport.html', {'msg': 'Search credentials are missing', 'uname':user_name, 'stdnts': students})
            except:
                return render(request, 'htmlFile/A-initialreport.html', {'msg': 'Fields are required', 'uname':user_name, 'stdnts': students})
        return render(request, "htmlFile/A-initialreport.html", {'uname': user_name, 'stdnts': students})
    return redirect('index')

def massreport(request):
    global user_role
    global user_name
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            date = request.POST.get("date")
            course = request.POST.get("whichcourse")
            status = request.POST.get("status")
            try:
                if date and course:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    if status:
                        cursor.execute(f'''
                        select studentcourse.s_id,student.s_name, student.s_dept, student.s_semester, student.s_section, student.s_email,course.C_name,Attendance.Atten_Status,Date(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where C_name="{course}" and Atten_Status="{status}" and Date(Atten_datetime)="{date}";

                        ''')
                    else:
                        cursor.execute(f'''
                        select studentcourse.s_id,student.s_name, student.s_dept, student.s_semester, student.s_section, student.s_email,course.C_name,Attendance.Atten_Status,Date(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where C_name="{course}" and Date(Atten_datetime)="{date}";

                        ''')
                    results = cursor.fetchall()
                    data = []
                    results = list(results)
                    for result in results:
                        temp_data = {}
                        temp_data['id'] = result[0]
                        temp_data['name'] = result[1]
                        temp_data['dept'] = result[2]
                        temp_data['sem'] = result[3]
                        temp_data['sec'] = result[4]
                        temp_data['email'] = result[5]
                        temp_data['course'] = result[6]
                        temp_data['status'] = result[7]
                        temp_data['date'] = str(result[8])
                        data.append(temp_data)
                    return render(request, 'htmlFile/A-massreport.html', {'data': data, 'uname':user_name, 'date':date})
                else:    
                    return render(request, 'htmlFile/A-massreport.html', {'msg': 'Search credentials are missing', 'uname':user_name, 'date':date})
            except:
                return render(request, 'htmlFile/A-massreport.html', {'msg': 'Fields are required', 'uname':user_name, 'date':date})    
        return render(request, 'htmlFile/A-massreport.html', {'uname': user_name})
    return redirect('index')

def massreport1(request):
    global user_role
    global user_name
    if user_role == "admin":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            date = request.POST.get("date")
            course = request.POST.get("whichcourse")
            semester = request.POST.get("Semester")
            section = request.POST.get("Section")
            try:
                if date and course and semester and section:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    cursor.execute(f'''
                    select studentcourse.s_id,student.s_name, student.s_Fathername, student.s_dept, student.s_section, student.s_semester, student.s_email,course.C_name,Attendance.Atten_Status,Date(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where C_name="{course}" and s_semester="{semester}" and s_section="{section}" and Date(Atten_datetime)="{date}";
                    ''')
                    results = cursor.fetchall()
                    data = []
                    results = list(results)
                    for result in results:
                        temp_data = {}
                        temp_data['id'] = result[0]
                        temp_data['name'] = result[1]
                        temp_data['fname'] = result[2]
                        temp_data['dept'] = result[3]
                        temp_data['sec'] = result[4]
                        temp_data['sem'] = result[5]
                        temp_data['email'] = result[6]
                        temp_data['course'] = result[7]
                        temp_data['status'] = result[8]
                        temp_data['date'] = str(result[9])
                        data.append(temp_data)
                    return render(request, 'htmlFile/A-massreport1.html', {'data': data, 'uname':user_name, 'date':date})
                else:    
                    return render(request, 'htmlFile/A-massreport1.html', {'msg': 'Search credentials are missing', 'uname':user_name, 'date':date})
            except:
                return render(request, 'htmlFile/A-massreport1.html', {'msg': 'Fields are required', 'uname':user_name, 'date':date})
        return render(request, 'htmlFile/A-massreport1.html', {'uname':user_name})
    return redirect('index')

def teacherlogin(request):
    global user_role
    global user_name
    if user_role == "":
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("pass")
            try:
                cursor = connection.cursor()
                cursor.execute(f'''
                    select t_name, t_id from teacher where t_name = "{username}" and t_password="{password}"
                ''')
                user = cursor.fetchone()
                if user:
                    uname = user[0]
                    user_name = user[0]
                    user_role = 'teacher'
                    return redirect('T-dashboard')            
                else:
                    print("Not found")
            except Exception as e:
                print(e)
        return render(request, 'htmlFile/T-teacherlogin.html')
    elif user_role=='teacher':
        return redirect('T-dashboard')
    return redirect('index')


def Tdashboard(request):
    global user_role
    global user_name
    cursor = connection.cursor()
    cursor.execute(f'''
    select s_name from student
    ''')
    students = []
    stds = cursor.fetchall()
    stds = list(stds)
    for std in stds:
        std = str(std)
        std = std.strip("(")
        std = std.strip(")")
        std = std.strip(',')
        std = std.strip("'")
        students.append(std)
    if user_role == "teacher":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            date = request.POST.get("date")
            std = request.POST.get("st_name")
            if date and std:
                year, month = date.split('-')
                """
                Fetching monthly data
                """
                cursor = connection.cursor()
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="present" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                present = len(results)
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="absent" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                absent = len(results)

                """
                Fetching yearly data
                """
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="present" and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                ypresent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in ypresent:
                        ypresent[mon] = 1
                    else:
                        ypresent[mon] = ypresent[mon] + 1
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{std}" and Atten_Status="absent" and year(Attendance.Atten_datetime) = '{year}' ;
                ''')
                results = cursor.fetchall()
                yabsent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in yabsent:
                        yabsent[mon] = 1
                    else:
                        yabsent[mon] = yabsent[mon] + 1
                
                def Union(lst1, lst2):
                    final_list = list(set(lst1) | set(lst2))
                    return final_list
                pkeys = list(ypresent.keys())
                akeys = list(yabsent.keys())
                keys = Union(pkeys, akeys)
            return render(request, 'htmlFile/T-dashboard.html', {'uname':user_name, 'present':present, 'absent':absent, 'ypresent': json.dumps(ypresent), 'yabsent': json.dumps(yabsent), 'keys':json.dumps(keys), 'date':date, 'stdnts':students})
        return render(request, 'htmlFile/T-dashboard.html', {'uname':user_name, 'present':11, 'absent':12, 'ypresent': json.dumps({
            'june' : 15,
            'may' : 12
        }), 'yabsent': json.dumps({
            'june' : 15,
            'may' : 18
        }), 'keys':json.dumps(['june', 'may']), 'stdnts':students})
    return redirect('index')

def teacherdashboard(request):
    global user_role
    global user_name
    if request.GET.get('logoutbtn'):
        user_role=""
        user_name = ""
        return redirect('index')
    if user_role == "teacher":
        cursor = connection.cursor()
        cursor.execute(f'''
            select * from teacher where t_name = "{user_name}"
        ''')
        result = cursor.fetchone()
        if result:
            user_details = {}
            user_details['name'] = result[1]
            user_details['gender'] = result[2]
            user_details['qualification'] = result[3]
            user_details['design'] = result[4]
            user_details['email'] = result[5]
            user_details['dep'] = result[6]
            user_details['cell_no'] = result[7]
        return render(request, 'htmlFile/T-teacherdashboard.html', {'uname':user_name, 'user':user_details})
    return redirect('index')

def Tattendance(request):
    global user_role
    global user_name
    if user_role == "teacher":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            date = request.POST.get("date")
            course = request.POST.get("whichcourse")
            status = request.POST.get("status")
            try:
                if date and course:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    if status:
                        cursor.execute(f'''
                        select studentcourse.s_id,student.s_name, student.s_dept, student.s_semester, student.s_section, student.s_email,course.C_name,Attendance.Atten_Status,Date(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where C_name="{course}" and Atten_Status="{status}" and Date(Atten_datetime)="{date}";

                        ''')
                        
                    else:
                        cursor.execute(f'''
                        select studentcourse.s_id,student.s_name, student.s_dept, student.s_semester, student.s_section, student.s_email,course.C_name,Attendance.Atten_Status,Date(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where C_name="{course}" and Date(Atten_datetime)="{date}";

                        ''')
                    results = cursor.fetchall()
                    data = []
                    results = list(results)
                    for result in results:
                        temp_data = {}
                        temp_data['id'] = result[0]
                        temp_data['name'] = result[1]
                        temp_data['dept'] = result[2]
                        temp_data['sem'] = result[3]
                        temp_data['sec'] = result[4]
                        temp_data['email'] = result[5]
                        temp_data['course'] = result[6]
                        temp_data['status'] = result[7]
                        temp_data['date'] = str(result[8])
                        data.append(temp_data)
                    return render(request, 'htmlFile/T-attendance.html', {'data': data, 'uname':user_name, 'date':date})
                else:    
                    return render(request, 'htmlFile/T-attendance.html', {'msg': 'Search credentials are missing', 'uname':user_name, 'date':date})
            except:
                return render(request, 'htmlFile/T-attendance.html', {'msg': 'Fields are required', 'uname':user_name, 'date':date})
        return render(request, 'htmlFile/T-attendance.html', {'uname':user_name})
    return redirect('index')

def Tstudentreport(request):
    global user_role
    global user_name
    cursor = connection.cursor()
    cursor.execute(f'''
    select s_name from student
    ''')
    students = []
    stds = cursor.fetchall()
    stds = list(stds)
    for std in stds:
        std = str(std)
        std = std.strip("(")
        std = std.strip(")")
        std = std.strip(',')
        std = std.strip("'")
        students.append(std)
    if user_role == "teacher":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            st_name = request.POST.get("st_name")
            course = request.POST.get("whichcourse")
            sec = request.POST.get("Section")

            try:
                if st_name and course and sec:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    cursor.execute(f'''
                    select studentcourse.s_id,student.s_name,student.s_dept, student.s_email, student.s_semester, student.s_section, course.C_name,Attendance.Atten_Status,Attendance.Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{st_name}" and C_name= "{course} and s_semester={sec}";
                    ''')
                    results = cursor.fetchall()
                    result = {}
                    if len(results) > 0:
                        print("Yes man")
                        result['s_id'] = results[0][0]
                        result['s_name'] = results[0][1]
                        result['s_dept'] = results[0][2]
                        result['s_email'] = results[0][3]
                        result['s_semester'] = results[0][4]
                        result['s_section'] = results[0][5]
                        result['s_totalCLasses'] = len(results)
                        result['s_presentClassses'] = 0
                        result['s_absentClassses'] = 0
                        for r in results:
                            if r[7] == 'present':
                                result['s_presentClassses'] = result['s_presentClassses'] + 1
                            elif r[7] == 'absent':
                                result['s_absentClassses'] = result['s_absentClassses'] + 1
                        return render(request, 'htmlFile/T-studentreport.html', {'student': result, 'uname':user_name, 'stdnts':students})
                    return render(request, 'htmlFile/T-studentreport.html', {'msg': "No record found", 'uname':user_name, 'stdnts':students})
                else:    
                    return render(request, 'htmlFile/T-studentreport.html', {'msg': 'Search credentials are missing', 'uname':user_name, 'stdnts':students})
            except:
                return render(request, 'htmlFile/T-studentreport.html', {'msg': 'Fields are required', 'uname':user_name, 'stdnts':students})
        return render(request, "htmlFile/T-studentreport.html", {'uname':user_name, 'stdnts':students})
    return redirect('index')

def Studentlogin(request):
    global user_role
    global user_name
    if user_role == "":
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("pass")
            try:
                cursor = connection.cursor()
                cursor.execute(f'''
                    select s_name, s_id from student where s_name = "{username}" and s_password="{password}"
                ''')
                user = cursor.fetchone()
                print(user)
                if user:
                    uname = user[0]
                    user_name = user[0]
                    user_role = 'student'
                    return redirect('S-dashboard')            
                else:
                    print("Not found")
            except Exception as e:
                print(e)
        return render(request, 'htmlFile/S-Studentlogin.html')
    elif user_role=='admin':
        return redirect('S-dashboard')
    return redirect('index')
    # return render(request, 'htmlFile/S-Studentlogin.html')

def S_dashboard(request):
    global user_role
    global user_name
    if user_role == "student":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index') 
        if request.method == 'POST':
            date = request.POST.get("date")
            if date:
                year, month = date.split('-')
                """
                Fetching monthly data
                """
                cursor = connection.cursor()
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{user_name}" and Atten_Status="present" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                present = len(results)
                cursor.execute(f'''
                select studentcourse.s_id, monthname(Attendance.Atten_datetime), year(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{user_name}" and Atten_Status="absent" and month(Attendance.Atten_datetime) = '{month}' and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                absent = len(results)

                """
                Fetching yearly data
                """
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{user_name}" and Atten_Status="present" and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                ypresent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in ypresent:
                        ypresent[mon] = 1
                    else:
                        ypresent[mon] = ypresent[mon] + 1
                cursor.execute(f'''
                select monthname(Attendance.Atten_datetime) as Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{user_name}" and Atten_Status="absent" and year(Attendance.Atten_datetime) = '{year}';
                ''')
                results = cursor.fetchall()
                yabsent = {}
                for mon in results:
                    mon = str(mon)
                    mon = mon.strip("(")
                    mon = mon.strip(")")
                    mon = mon.strip(',')
                    mon = mon.strip("'")
                    if mon not in yabsent:
                        yabsent[mon] = 1
                    else:
                        yabsent[mon] = yabsent[mon] + 1
                
                def Union(lst1, lst2):
                    final_list = list(set(lst1) | set(lst2))
                    return final_list
                pkeys = list(ypresent.keys())
                akeys = list(yabsent.keys())
                keys = Union(pkeys, akeys)
            return render(request, 'htmlFile/S-dashboard.html', {'uname':user_name, 'present':present, 'absent':absent, 'ypresent': json.dumps(ypresent), 'yabsent': json.dumps(yabsent), 'keys':json.dumps(keys), 'date':date})
        return render(request, 'htmlFile/S-dashboard.html', {'uname':user_name, 'present':11, 'absent':12, 'ypresent': json.dumps({
            'june' : 15,
            'may' : 12
        }), 'yabsent': json.dumps({
            'june' : 15,
            'may' : 18
        }), 'keys':json.dumps(['june', 'may'])})
    return redirect('index')

def Sdashboard(request):
    global user_role
    global user_name
    if user_role == "student":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        cursor = connection.cursor()
        cursor.execute(f'''
            select * from student where s_name = "{ user_name }"
        ''')
        result = cursor.fetchone()
        print(result)
        if result:
            user_details = {}
            user_details['name'] = result[1]
            user_details['fname'] = result[2]
            user_details['gender'] = result[3]
            user_details['qual'] = result[4]
            user_details['email'] = result[5]
            user_details['dept'] = result[6]
            user_details['cell_no'] = result[7]
            user_details['sec'] = result[8]
            user_details['sem'] = result[9]
        return render(request, 'htmlFile/S-Studentdashboard.html', {'uname':user_name, 'user':user_details})
    return redirect('index')

def studentreport(request):
    global user_role
    global user_name
    if user_role == "student":
        if request.GET.get('logoutbtn'):
            user_role=""
            user_name = ""
            return redirect('index')
        if request.method == 'POST':
            course = request.POST.get("whichcourse")
            try:
                if course:
                    # student = Student.objects.get(s_id=s_id)
                    # attendance = Attendance.objects.get(sc_id = s_id)
                    # print(attendance)
                    cursor = connection.cursor()
                    cursor.execute(f'''
                    select studentcourse.s_id,student.s_name,student.s_dept, student.s_email, student.s_semester, student.s_section, course.C_name,Attendance.Atten_Status,Attendance.Atten_datetime from Attendance left outer join studentcourse on studentcourse.SC_id=Attendance.sc_id left outer join student on student.s_id=studentcourse.S_id left outer join course on course.C_id=studentcourse.c_id where s_name= "{user_name}" and C_name= "{course}";
                    ''')
                    results = cursor.fetchall()
                    result = {}
                    if len(results) > 0:
                        result['s_id'] = results[0][0]
                        result['s_name'] = results[0][1]
                        result['s_dept'] = results[0][2]
                        result['s_email'] = results[0][3]
                        result['s_semester'] = results[0][4]
                        result['s_section'] = results[0][5]
                        result['s_totalCLasses'] = len(results)
                        result['s_presentClassses'] = 0
                        result['s_absentClassses'] = 0
                        for r in results:
                            if r[7] == 'present':
                                result['s_presentClassses'] = result['s_presentClassses'] + 1
                            elif r[7] == 'absent':
                                result['s_absentClassses'] = result['s_absentClassses'] + 1
                        return render(request, 'htmlFile/S-studentreport.html', {'student': result, 'uname':user_name})
                    return render(request, 'htmlFile/S-studentreport.html', {'msg': "No record found", 'uname':user_name})
                else:    
                    return render(request, 'htmlFile/S-studentreport.html', {'msg': 'Search credentials are missing', 'uname':user_name})
            except:
                return render(request, 'htmlFile/S-studentreport.html', {'msg': 'Fields are required', 'uname':user_name})
        return render(request, "htmlFile/S-studentreport.html", {'uname': user_name})
    return redirect('index')