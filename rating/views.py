from urllib.parse import parse_qsl, parse_qs

from django.contrib.auth import authenticate as authen
from django.contrib.auth import login as login_test
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import logout, login
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentForm
from .models import Group, Student
import json


@csrf_exempt
def student(request):
    if request.user.is_authenticated:
        gr = Group.objects.get(curator=request.user.id)
        return render(request, 'rating/student.html', {'group': gr})
    else:
        return render(request,
                      'rating/index.html',
                      {}
                      )


@csrf_exempt
def group(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = authen(username=username, password=password)

        if user:
            if user.is_active:
                login_test(request, user)
                gr = Group.objects.get(curator=user.id)

                return render(request, 'rating/group.html', {'group': gr})
        else:
            return redirect('groups')

    if request.user.is_authenticated:
        gr = Group.objects.get(curator=request.user.id)
        return render(request, 'rating/group.html', {'group': gr})
    else:
        return render(request,
                      'rating/index.html',
                      {}
                      )


@csrf_exempt
def ajax_student_delete(request):
    if request.is_ajax():
        if request.method == 'POST':
            params = request.POST.dict()
            stud = Student.objects.get(pk=int(params['student_id']))
            stud.delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@csrf_exempt
def ajax_group(request, pk):
    if request.method == 'POST':
        if request.is_ajax():
            params = request.POST.dict()
            print(params)

            form = StudentForm(request.POST)
            print('form=', form)
            if form.is_valid():
                group = params.pop('group')
                params.pop('csrfmiddlewaretoken')
                params['group'] = Group.objects.get(name=group)
                stud = Student.objects.create(**params)
                return HttpResponse(json.dumps({'success': True}), content_type='application/json')
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')

        username = request.POST['user']
        password = request.POST['pass']
        user = authen(username=username, password=password)

        if user:
            if user.is_active:
                login_test(request, user)
                return render(request, 'rating/group.html', {'pk': pk})
        else:
            return render(request, 'rating/group.html', {'pk': pk})

    all_students = Student.objects.filter(group=pk)
    # data = serializers.serialize('json', all_students)
    return JsonResponse([stud.serialize for stud in all_students], safe=False)


@csrf_exempt
def ajax_students(request):
    all_students = Student.objects.all()
    # data = serializers.serialize('json', all_students)
    return JsonResponse([stud.serialize for stud in all_students], safe=False)


def logout_view(request, *args, **kwargs):
    logout(request, *args, **kwargs)
    return redirect('/')


def login_view(request, *args, **kwargs):
    # login(request, *args, **kwargs)
    return render(
        request,
        'registration/login.html',
        {
            'curator': 'curator', }
    )


def index(request):
    return render(
        request,
        'rating/index.html',
        {}
    )


class GroupListView(generic.ListView):
    model = Group

    context_object_name = 'my_groups_list'

    def get_queryset(self):
        return Group.objects.all()

    template_name = 'rating/index.html'


class GroupDetailView(generic.DetailView):
    model = Group
