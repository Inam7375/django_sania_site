from django.shortcuts import render, redirect
from .forms import StudentForm

# Create your views here.

def Addstudent(request):
    # AddStudent = StudentForm
    # print("Save")
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/S-dashboard")
            except:
                return render(request,'A-Addstudent.html',{'form':form})
        else:
            form = StudentForm()
    return render(request,'A-Addstudent.html',{'form':form})

def Addteacher(request):
    AddTeacher = Addteacher.objects.all()
    print("Save")
    return render(request,'A-Addteacher.html', {'Addteacher':AddTeacher})

def Userregistration(request):
    UserRegistration = Userregistration.objects.all()
    print("Save")
    return render(request,'SignupForm.html', {'Userregistration':UserRegistration})