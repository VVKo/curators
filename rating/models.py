from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=3)
    curator = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} група".format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'group': self.name,
            'students': self.get_students,
        }

    @property
    def get_students(self):
        students = Student.objects.filter(group=self.id)
        return [stud.get_student for stud in students]


class Student(models.Model):
    last_name = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True, default='')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default='')

    def __str__(self):
        return "{} {} {} {} група".format(self.last_name, self.first_name, self.middle_name, self.group.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'stud': self.get_student,
            'group': str(self.group),
            'group_id': self.group.id,
        }

    @property
    def get_student(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)
