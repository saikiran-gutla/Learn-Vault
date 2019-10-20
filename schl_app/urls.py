from django.conf.urls import url, include
from schl_app.views import student_register, \
    teacher_register, \
    student_login_view, \
    student_logout_view, \
    student_home, \
    teacher_login_view, \
    teacher_logout_view, \
    teacher_home, \
    test_questions, home_page, student_videos, student_results,\
    StoreTestData,\
    StudentResultsView ,\
    TeacherResultsView,\
    Student_Profile,\
    Teacher_Profile

urlpatterns = [
    url(r'^stu_register/', student_register, name='student register'),
    url(r'^teacher_register/', teacher_register, name='teacher register'),
    url(r'^student_home/', student_home, name='student home'),
    url(r'^student_login/', student_login_view, name='student login'),
    url(r'^student_logout/', student_logout_view, name='student logout'),
    url(r'^teacher_home/', teacher_home, name='teacher home'),
    url(r'^teacher_login/', teacher_login_view, name='teacher login'),
    url(r'^teacher_logout/', teacher_logout_view, name='teacher logout'),
    url(r'^test/', test_questions, name='test questions'),
    url(r'^home_page/', home_page, name='home page'),
    url(r'^student_videos/', student_videos, name='student videos'),
    url(r'^student_results/', student_results, name='student results'),
    url(r'^store_test_data/', StoreTestData, name='Test Data'),
    url(r'^results/', StudentResultsView, name='Student Results View'),
    url(r'^all_results/', TeacherResultsView, name='Teacher Results View'),
    url(r'^student_profile/', Student_Profile, name='Student Profile View'),
    url(r'^teacher_profile/', Teacher_Profile, name='Teacher Profile View'),
]
