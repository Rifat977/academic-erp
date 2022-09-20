from django.urls import path
from . import views

app_name="backend"
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),

    #teacher
        #attendance
    path('teacher/<slug:teacher_id>/<int:choice>/classes/', views.t_class, name='classes'),
    path('teacher/<int:assign_id>/ClassDates/', views.t_class_date, name='class_date'),
    path('teacher/<int:assign_id>/Students/attendance/', views.t_student, name='students'),
    path('teacher/<int:ass_c_id>/attendance/', views.t_attendance, name='attendance'),
    path('teacher/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),
    path('teacher/<int:ass_c_id>/Cancel/', views.cancel_class, name='cancel_class'),
    path('teacher/<int:ass_c_id>/Edit_att/', views.edit_attendance, name='edit_attendance'),
    path('teacher/<int:assign_id>/Extra_class/', views.extra_class, name='extra_class'),
    path('teacher/<slug:assign_id>/Extra_class/confirm/', views.e_confirm, name='e_confirm'),
        #marks
    path('teacher/<int:assign_id>/marks_list/', views.marks_list, name='marks_list'),
    path('teacher/<int:assign_id>/Students/Marks/', views.student_marks, name='student_marks'),

]