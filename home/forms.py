from django import forms
from .models import Student, Attendance

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

class Attendance(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = '__all__'