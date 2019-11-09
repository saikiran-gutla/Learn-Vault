# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from schl_app.models import StudentDetails, \
    TeacherDetails, \
    TestData,\
	Video


class StudentDetailsAdmin(admin.ModelAdmin):
    model = StudentDetails
    list_display = ('student_name', 'student_id')


admin.site.register(StudentDetails, StudentDetailsAdmin)


class TeacherDetailsAdmin(admin.ModelAdmin):
    model = TeacherDetails
    list_display = ('teacher_name', 'teacher_id')


admin.site.register(TeacherDetails, TeacherDetailsAdmin)


class TestDataAdmin(admin.ModelAdmin):
    model = TestData
    list_display = ('Student_Name', 'Test_Date')
    search_field = ('Student_Name',)


admin.site.register(TestData, TestDataAdmin)


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ('name',)
    search_field = ('name',)
admin.site.register(Video, VideoAdmin)
