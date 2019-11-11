# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import random
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from schl_app.models import StudentDetails, \
    TeacherDetails, \
    TestData, Video
from schl_app.questions import questions_list
from .forms import VideoForm
from django.conf import settings


def home_page(request):
    return render(request, 'index.html', {})


@csrf_protect
def student_register(request):
    context = {}
    stud_id, tech_id = gen_rand_id()
    try:
        if request.method == "POST":
            first_name, last_name, user_email, password, student_DOB, \
            stu_father_name, mobile_no, gender, standard = (request.POST['first_name'],
                                                            request.POST['last_name'],
                                                            request.POST['user_email'],
                                                            request.POST['password'],
                                                            request.POST['student_DOB'],
                                                            request.POST['stu_father_name'],
                                                            request.POST['mobile_no'],
                                                            request.POST['gender'],
                                                            request.POST['standard'])
            user_name = first_name + last_name
            stu_profile = User.objects.create_user(username=user_name,
                                                   email=user_email,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   password=password)
            stu_profile = StudentDetails.objects.create(student_name=stu_profile,
                                                        mail_id=user_email, student_password=password,
                                                        student_DOB=student_DOB, student_id=stud_id,
                                                        standard=standard, stu_father_name=stu_father_name,
                                                        gender=gender, mobile_no=mobile_no)
            context = {'student': stu_profile}
            msg = user_name + " created successfully with ID : " + stud_id + "\nLogin into your Student account from Login Page"
            messages.success(request, msg)
            return render(request, 'index.html', context)
        else:
            return render(request, 'student_register.html', context)
    except:
        return render(request, 'index.html',
                      messages.success(request, "Entered Email Already Exist..Try with another Email"))


@csrf_protect
def teacher_register(request):
    context = {}
    stud_id, tech_id = gen_rand_id()
    try:
        if request.method == "POST":
            first_name, last_name, user_email, password, mobile_no, gender, teacher_DOB, teacher_father_name = (
                request.POST['first_name'],
                request.POST['last_name'],
                request.POST['user_email'],
                request.POST['password'],
                request.POST['mobile_no'],
                request.POST['gender'],
                request.POST['teacher_DOB'],
                request.POST['teacher_father_name'])
            user_name = first_name + last_name
            teacher_profile = User.objects.create_user(username=user_name,
                                                       email=user_email,
                                                       first_name=first_name,
                                                       last_name=last_name,
                                                       password=password,
                                                       is_staff=True)
            teacher_profile = TeacherDetails.objects.create(teacher_name=teacher_profile,
                                                            teacher_id=tech_id,
                                                            gender=gender,
                                                            mobile_no=mobile_no,
                                                            teacher_mail_id=user_email,
                                                            teacher_password=password,
                                                            tec_father_name=teacher_father_name,
                                                            teacher_DOB=teacher_DOB)
            context = {'teacher': teacher_profile}
            msg = user_name + " created successfully with ID : " + tech_id + '\nLogin into your Teacher account from Login Page'
            messages.success(request, msg)
            return render(request, 'index.html', context)
        else:
            return render(request, 'teacher_register.html', context)
    except:
        return render(request, 'index.html',
                      messages.success(request, "Entered Email Already Exist..Try to register again with another Email"))


def student_login_view(request):
    return render(request, 'student_login.html')


def student_home(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_name = request.user
            return render(request, 'student_home.html', {'user': user_name})
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('home page')
    else:
        user_name = request.user
        return render(request, 'student_home.html', {'user': user_name})


def teacher_login_view(request):
    return render(request, 'teacher_login.html')


def teacher_home(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_name = request.user
            return render(request, 'teacher_home.html', {'user': user_name})
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('home page')
    else:
        user_name = request.user
        return render(request, 'teacher_home.html', {'user': user_name})


def gen_rand_id():
    stud_id = "STD"
    tech_id = "TCH"

    def gen_id():
        rand_id = ""
        for i in range(4):
            id = random.randint(0, 9)
            rand_id += str(id)
        return rand_id

    stud_id += gen_id()
    tech_id += gen_id()
    return stud_id, tech_id


@login_required
def student_videos(request):
    return render(request, 'student_videos.html', {})


@login_required
def student_results(request):
    return render(request, 'student_results.html', {})


@login_required
def test_questions(request):
    questions = []
    if request.method == 'GET':
        for qstn in questions_list:
            questions.append({'Question_No': qstn['q_no'],
                              'Lable_No': qstn['lno'],
                              'Question': qstn['question'],
                              'Choices': qstn['choices'],
                              'Hint': qstn['hint']})
            random.shuffle(questions)

        return render(request, 'test_questions.html', {'question': questions})


@login_required
def StoreTestData(request):
    if request.method == 'POST':
        username = request.user
        data = request.POST
        for dt in data:
            TestData.objects.create(Student_Name=username, Test_Data=dt, Test_Date=date.today())
        return redirect('Student Results View')


@login_required
def StudentResultsView(request):
    if request.method == "GET":
        results = {}
        results_list = []
        correct_ans = {}
        qn_list = questions_list
        if request.user.is_active is True and request.user.is_staff is not True:
            try:
                testdata_obj = TestData.objects.filter(Student_Name__username=request.user).order_by('-id')
                for test_data in testdata_obj:
                    student_details = StudentDetails.objects.get(student_name__username=test_data.Student_Name.username)
                    results[test_data.id] = {
                        'student_name': test_data.Student_Name.username,
                        'student_id': student_details.student_id,
                        'score': 0,
                        'class': student_details.standard,
                        'test_date': str(test_data.Test_Date)
                    }
                    correct_ans[test_data.id] = {'score': 0}
                    testdata_json = json.loads(test_data.Test_Data)
                    for testdata in testdata_json:
                        print(testdata['hint'])
                        for qstn in qn_list:
                            if testdata['question'] == qstn['question'] and testdata['ans'] == qstn['answer'] and \
                                    testdata['hint'] == "checked":
                                results[test_data.id]['score'] += 4
                                correct_ans[test_data.id]['score'] += 4
                            elif testdata['question'] == qstn['question'] and testdata['ans'] == qstn['answer'] and \
                                    testdata['hint'] == "unchecked":
                                results[test_data.id]['score'] += 5
                                correct_ans[test_data.id]['score'] += 5
                            elif testdata['question'] == qstn['question'] and testdata['ans'] != qstn['answer'] and \
                                    testdata['hint'] == "checked":
                                results[test_data.id]['score'] -= 1
                                correct_ans[test_data.id]['score'] -= 1
                            elif testdata['question'] == qstn['question'] and testdata['ans'] != qstn['answer'] and \
                                    testdata['hint'] == "unchecked":
                                results[test_data.id]['score'] += 0
                                correct_ans[test_data.id]['score'] += 0
                        # if testdata['hint'] == "unchecked":
                        #     results[test_data.id]['score'] += 5
                        #     correct_ans[test_data.id]['score'] += 5
                        # elif testdata['hint'] == "checked":
                        #     results[test_data.id]['score'] -= 1
                        #     correct_ans[test_data.id]['score'] -= 1

                    for scr in correct_ans.values():
                        if scr['score'] >= 10:
                            results[test_data.id].update({'remark': "PASS"})
                        elif scr['score'] == 0:
                            results[test_data.id].update({'remark': "FAIL"})
                        else:
                            results[test_data.id].update({'remark': "FAIL"})

                results_list.append(results)
            except:
                results_list.append({
                    "No_Data": "No Results Found"
                })
        return render(request, 'student_results.html', {'result': results_list})


@login_required
def TeacherResultsView(request):
    if request.method == "GET":
        results = {}
        results_list = []
        correct_ans = {}
        qn_list = questions_list
        user_obj = User.objects.filter(is_staff=False)
        users_list = [u.username for u in user_obj]
        if request.user.is_staff == True:
            try:
                testdata_obj = TestData.objects.filter(Student_Name__username__in=users_list).order_by('-id')
                for test_data in testdata_obj:
                    student_details = StudentDetails.objects.get(student_name__username=test_data.Student_Name.username)
                    results[test_data.id] = {
                        'student_name': test_data.Student_Name.username,
                        'student_id': student_details.student_id,
                        'score': 0,
                        'class': student_details.standard,
                        'test_date': str(test_data.Test_Date)
                    }
                    correct_ans[test_data.id] = {'score': 0}
                    testdata_json = json.loads(test_data.Test_Data)
                    for testdata in testdata_json:
                        for qstn in qn_list:
                            if testdata['question'] == qstn['question'] and testdata['ans'] == qstn['answer']:
                                results[test_data.id]['score'] += 1
                                correct_ans[test_data.id]['score'] += 1

                    for scr in correct_ans.values():
                        if scr['score'] >= 2:
                            results[test_data.id].update({'remark': "PASS"})
                        elif scr['score'] == 0:
                            results[test_data.id].update({'remark': "FAIL"})
                        else:
                            results[test_data.id].update({'remark': "FAIL"})

                results_list.append(results)
            except:
                results_list.append({
                    "No_Data": "No Results Found"
                })
        return render(request, 'teacher_results_view.html', {'result': results_list})


@login_required
def Student_Profile(request):
    if request.method == 'GET':
        details = {}
        details_list = []
        profile = StudentDetails.objects.get(student_name__username=request.user)
        details = {
            'Name': profile.student_name.username,
            'Id': profile.student_id,
            'Gender': profile.gender,
            'Mobile_No': profile.mobile_no,
            'Email_Id': profile.mail_id,
            'DOB': str(profile.student_DOB),
            'Standard': profile.standard,
            'Father_Name': profile.stu_father_name
        }

        details_list.append(details)
        return render(request, 'student_profile.html', {'profiles': details_list})


@login_required
def Teacher_Profile(request):
    if request.method == 'GET':
        details = {}
        details_list = []
        profile = TeacherDetails.objects.get(teacher_name__username=request.user)
        details = {
            'Name': profile.teacher_name.username,
            'Id': profile.teacher_id,
            'Gender': profile.gender,
            'Mobile_No': profile.mobile_no,
            'Email_Id': profile.teacher_mail_id,
            'DOB': str(profile.teacher_DOB),
            'Father_Name': profile.tec_father_name
        }

        details_list.append(details)
        print(details_list)
        return render(request, 'teacher_profile.html', {'profiles': details_list})


def contact_us(request):
    return render(request, 'contact_us.html', {})


@login_required
def student_profile_update(request):
    student = StudentDetails.objects.get(student_name__username=request.user)
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        user.username = request.POST['Name']
        # student.student_id = request.POST['Id']
        student.stu_father_name = request.POST['Father_Name']
        student.mail_id = request.POST['Email_Id']
        student.mobile_no = request.POST['Mobile_No']
        student.student_DOB = request.POST['DOB']
        user.save()
        student.save()
        return redirect("Student Profile View")
    return render(request, 'student_profile.html', {'student': model_to_dict(student)})


@login_required
def teacher_profile_update(request):
    teacher = TeacherDetails.objects.get(teacher_name__username=request.user)
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        user.username = request.POST['Name']
        # teacher.teacher_id = request.POST['Id']
        teacher.tec_father_name = request.POST['Father_Name']
        teacher.teacher_mail_id = request.POST['Email_Id']
        teacher.mobile_no = request.POST['Mobile_No']
        teacher.teacher_DOB = request.POST['DOB']
        user.save()
        teacher.save()
        return redirect("Teacher Profile View")
    return render(request, 'teacher_profile.html', {'teacher': model_to_dict(teacher)})


def Teac_contact(request):
    return render(request, 'tcontact.html', {})


def Logout(request):
    logout(request)
    return redirect('/')


@login_required
def post_video(request):
    lastvideo = Video.objects.last()
    videofile = lastvideo.videofile

    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {'videofile': videofile,
               'form': form
               }

    return render(request, 'video_upload.html', context)


@login_required
def get_videos(request):
    video_url = []
    if request.method == "GET":
        videos_qs = Video.objects.all()
        for videos in videos_qs:
            video_url.append(videos.videofile)
            print(video_url)
        return render(request, 'student_videos.html', {'urls': video_url})
