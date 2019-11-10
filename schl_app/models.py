# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
import os


# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=500)
    videofile = models.FileField(upload_to='media/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)


class StudentDetails(models.Model):
    student_name = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=200, null=True)
    standard = models.CharField(max_length=200, null=True)
    stu_father_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    mail_id = models.CharField(max_length=200, null=True)
    student_password = models.CharField(max_length=200, null=True)
    student_DOB = models.DateField()

    class Meta:
        unique_together = ('mail_id',)

    def __str__(self):
        return "%s" % (self.student_name)


class TeacherDetails(models.Model):
    teacher_name = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    teacher_mail_id = models.CharField(max_length=40, null=True)
    teacher_password = models.CharField(max_length=25, null=True)
    teacher_DOB = models.DateField(null=True)
    tec_father_name = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = ('teacher_mail_id',)

    def __str__(self):
        return "%s" % (self.teacher_name)


class TestData(models.Model):
    Student_Name = models.ForeignKey(User, on_delete=models.CASCADE)
    Test_Data = models.TextField()
    Test_Date = models.DateField()

    def __str__(self):
        return "%s" % (self.Student_Name)
