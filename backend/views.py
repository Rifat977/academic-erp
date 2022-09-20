from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from .decorators import unauthenticated_user
from .models import Student, Teacher, Assign, AttendanceClass, AttendanceTotal, Attendance, StudentCourse, MarksClass
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_teacher:
        return render(request, 'teacher/dashboard.html')
    if request.user.is_student:
        return render(request, 'student/dashboard.html')
    if request.user.is_superuser:
        return redirect('admin/')
    return render(request, 'login.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('backend:dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('backend:login')

# Teacher Views

@login_required
def t_class(request, teacher_id, choice):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher/classes.html', {'teacher': teacher, 'choice': choice})

@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'teacher/class_date.html', {'att_list': att_list})

@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'teacher/students.html', {'att_list': att_list})


@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'teacher/attendance.html', context)


@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.course
    cl = ass.class_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(
                    course=cr, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=cr, student=s, status=status,
                               date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(course=cr, student=s, status=status,
                           date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('backend:class_date', args=(ass.id,)))


@login_required()
def edit_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.course
    att_list = Attendance.objects.filter(attendanceclass=assc, course=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'teacher/edit_attendance.html', context)

@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('backend:class_date', args=(assc.assign_id,)))

@login_required()
def extra_class(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
    }
    return render(request, 'teacher/extra_class.html', context)


@login_required()
def e_confirm(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    cr = ass.course
    cl = ass.class_id
    assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
    assc.save()

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        date = request.POST['date']
        a = Attendance(course=cr, student=s, status=status,
                       date=date, attendanceclass=assc)
        a.save()

    return HttpResponseRedirect(reverse('backend:classes', args=(ass.teacher_id, 1)))

@login_required()
def student_marks(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    sc_list = StudentCourse.objects.filter(
        student__in=ass.class_id.student_set.all(), course=ass.course)
    return render(request, 'teacher/student_marks.html', {'sc_list': sc_list})

@login_required()
def marks_list(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    m_list = MarksClass.objects.filter(assign=ass)
    return render(request, 'teacher/marks_list.html', {'m_list': m_list})
