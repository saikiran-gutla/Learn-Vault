# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from schl_app.models import StudentDetails,\
							TeacherDetails,\
							TestData
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from schl_app.questions import questions_list
import random
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from datetime import datetime,date
import ast
from django.forms.models import model_to_dict


def home_page(request):
	return render(request, 'index.html', {})


def student_videos(request):
	return render(request, 'student_videos.html', {})


def student_results(request):
	return render(request, 'student_results.html', {})


def student_register(request):
	context = {}
	stud_id, tech_id = gen_rand_id()
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
		# return render(request, 'student_login.html', context)
		return redirect('home page')
	else:
		return render(request, 'student_register.html', context)


def teacher_register(request):
	context = {}
	stud_id, tech_id = gen_rand_id()
	if request.method == "POST":
		first_name, last_name, user_email, password, mobile_no, gender, teacher_DOB, teacher_father_name= (request.POST['first_name'],
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
														teacher_mail_id = user_email,
														teacher_password = password,
														tec_father_name=teacher_father_name,
														teacher_DOB=teacher_DOB)
		context = {'teacher': teacher_profile}
		msg = user_name + " created successfully with ID : " + tech_id + '\nLogin into your Teacher account from Login Page'
		messages.success(request, msg)
		return redirect('home page')
		# return render(request, 'teacher_login.html', context)
	else:
		return render(request, 'teacher_register.html', context)


def student_login_view(request):
	return render(request, 'student_login.html')


def student_logout_view(request):
	logout(request)
	return redirect("student login")


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


def teacher_logout_view(request):
	logout(request)
	return redirect("teacher login")


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

def test_questions(request):
	questions = []
	if request.method == 'GET':
		for qstn in questions_list:
			questions.append({'Question': qstn['question'],
							  'Choices': qstn['choices']})
			random.shuffle(questions)

		return render(request, 'test_questions.html', {'question': questions})
	
def StoreTestData(request):
	if request.method == 'POST':
		username = request.user
		data = request.POST
		for dt in data:
			TestData.objects.create(Student_Name=username,Test_Data= dt,Test_Date=date.today())
		return redirect('Student Results View')

def StudentResultsView(request):
	if request.method == "GET":
		results = {}
		results_list = []
		correct_ans = 0
		wrong_ans = 0
		qn_list = questions_list
		if request.user.is_staff != True:
			testdata_obj = TestData.objects.filter(Student_Name=request.user).latest('id')
			test_data = model_to_dict(testdata_obj)
			testdata_json  = json.loads(test_data['Test_Data'])
			for testdata in testdata_json:
				for qstn in qn_list:
					if testdata['question'] == qstn['question'] and testdata['ans'] == qstn['answer']:
						correct_ans += 1
					elif testdata['question'] == qstn['question'] and testdata['ans'] != qstn['answer']:
						wrong_ans += 1

		student_details = StudentDetails.objects.get(student_name__username=request.user)
		results = {
				'student_name':student_details.student_name.username,
				'student_id':student_details.student_id,
				'score': correct_ans
				}      
		if correct_ans >= 2:
			results.update({'remark':"PASS"})
		else:
			results.update({'remark':"FAIL"})
		results_list.append(results)
		return render(request, 'student_results.html', {'result': results_list})

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
					correct_ans[test_data.id] = {'score':0}
					testdata_json  = json.loads(test_data.Test_Data)
					for testdata in testdata_json:
						for qstn in qn_list:
							if testdata['question'] == qstn['question'] and testdata['ans'] == qstn['answer']:
								results[test_data.id]['score'] += 1
								correct_ans[test_data.id]['score'] += 1
					
					for scr in correct_ans.values():
						if scr['score'] >= 2:
							results[test_data.id].update({'remark':"PASS"})
						elif scr['score'] == 0:
							results[test_data.id].update({'remark':"FAIL"})
						else:
							results[test_data.id].update({'remark':"FAIL"})							


				results_list.append(results)
			except:
				print("No Data")
		return render(request, 'teacher_results_view.html', {'result': results_list})

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

# def teacher_profile_update(request):
# 	if request.method == 'POST':
# 		username = request.user
# 		data = request.POST
# 		details = TeacherDetails.objects.get(teacher_name__username=request.user)
# 		for dt in data:
# 			details.teacher_name = dt['Name']
# 			details.save()
