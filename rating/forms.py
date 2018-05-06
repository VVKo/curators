from django.forms import ModelForm
from .models import Student, Group, BlockOne


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', ]


class BlockOneForm(ModelForm):
    class Meta:
        model = BlockOne
        fields = ['mark',]