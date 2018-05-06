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

    class Meta:
        ordering = ['last_name']

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
            'subjects': self.get_subjects,
            'marks': self.tabel,
            'rating': self.rating,
        }

    @property
    def get_student(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    @property
    def get_subjects(self):
        all_subjects = Subject.objects.filter(group=self.group)
        # print('all_subjects', [sub.name for sub in all_subjects])
        return [sub.serialize for sub in all_subjects]

    @property
    def get_marks(self):

        all_marks = BlockOne.objects.filter(person=self.id)
        # print('all_subjects', [mark.serialize for mark in all_marks])
        return [mark.serialize for mark in all_marks]

    @property
    def tabel(self):
        subj = self.get_subjects
        tab = list()
        for sub in subj:

            all_marks = BlockOne.objects.filter(person=self.id)
            mark = all_marks.filter(subject=sub['subj_id'])
            if mark:
                rezult = mark.values_list('mark')
                sub['mark'] = rezult[0][0]
            else:
                sub['mark'] = 0

            tab.append(sub)

        return tab

    @property
    def rating(self):
        subj = self.get_subjects
        first_sum, first_count = 0, 0
        second_sum, second_count = 0, 0
        for sub in subj:

            all_marks = BlockOne.objects.filter(person=self.id)
            mark = all_marks.filter(subject=sub['subj_id'])
            if mark:
                rezult = mark.values_list('mark')
                sub['mark'] = rezult[0][0]
            else:
                sub['mark'] = 0

            if sub['semester'] == '1':
                first_sum += sub['mark']
                first_count += 1

            if sub['semester'] == '2':
                second_sum += sub['mark']
                second_count += 1

        if first_count == 0:
            rating_first = 0
        else:
            rating_first = first_sum / first_count

        if second_count == 0:
            rating_second = 0
        else:
            rating_second = second_sum / second_count

        if first_count + second_count == 0:
            rating_total = 0
        else:
            rating_total = (first_sum + second_sum) / (first_count + second_count)

        return {'rating_first': rating_first, 'rating_second': rating_second,
                'rating_total': rating_total, }


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=False)
    semester = models.CharField(max_length=1, choices=(('1', 'перший семестр'), ('2', 'другий семестр')))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default='')

    def __str__(self):
        return "{} {}".format(self.name, self.semester)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'subj_id': self.id,
            'subject': self.__str__(),
            'semester': self.semester,
        }

    class Meta:
        ordering = ('semester',)


class BlockOne(models.Model):
    person = models.ForeignKey(Student, blank=False, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, blank=False, on_delete=models.CASCADE)
    mark = models.IntegerField(blank=False, choices=[(i, i) for i in range(1, 101)], default=0)

    def __str__(self):
        return "{} {} {}".format(self.person.get_student, self.subject.name, self.mark)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'person': self.person.get_student,
            'person_id': self.person.id,
            'subject': self.subject.name,
            'mark': self.mark,
            'sem': self.subject.semester,
        }

    class Meta:
        ordering = ('person', 'subject',)
        unique_together = ('person', 'subject',)
