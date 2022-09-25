from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date', 'status')
    ordering = ['assign', 'date']
    
# class AssignTimeInline(admin.TabularInline):
#     model = AssignTime
#     extra = 0

class AssignAdmin(admin.ModelAdmin):
    # inlines = [AssignTimeInline]
    list_display = ('class_id', 'course', 'teacher')

class AssignTimeAdmin(admin.ModelAdmin):
    list_display = ('assign', 'period', 'day')

class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0


class StudentCourseAdmin(admin.ModelAdmin):
    inlines = [MarksInline]
    list_display = ('student', 'course',)
    search_fields = ('student__name', 'course__name', 'student__class_id__id', 'student__class_id__dept__name')
    ordering = ('student__class_id__dept__name', 'student__class_id__id', 'student__USN')


admin.site.register(User, UserAdmin)
admin.site.register(Dept)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Assign, AssignAdmin)
admin.site.register(AssignTime, AssignTimeAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)
admin.site.register(AttendanceRange)
