from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='groups'),
    # path(r'login/', views.login_view, name='logout'),
    # path(r'login/', auth_views.login, {'authentication_form': CustomAuthenticationForm}, name='login'),
    path(r'logout/', views.logout_view, {'next_page': '/'}, name='logout'),
    path(r'group/', views.group,  name='group'),
    # path(r'group/<int:pk>', views.GroupDetailView.as_view(),  name='group-detail'),
    path(r'ajax/group/<int:pk>', views.ajax_group, name='ajax-group-detail'),
    path(r'group/ajax/student/delete', views.ajax_student_delete, name='ajax-student-delete'),
    # path(r'ajax/students/all', views.ajax_students, name='ajax-students-all'),

]