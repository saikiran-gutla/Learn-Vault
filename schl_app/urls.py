from django.conf.urls import url, include
from schl_app.views import student_register, \
    teacher_register, \
    student_login_view, \
    student_home, \
    teacher_login_view, \
    teacher_home, \
    test_questions, home_page, student_videos, \
    StoreTestData, \
    StudentResultsView, \
    TeacherResultsView, \
    Student_Profile, \
    Teacher_Profile, contact_us, \
    student_profile_update, \
    teacher_profile_update, student_results, Logout, post_video, get_videos,about_us

urlpatterns = [
    url(r'^stu_register/', student_register, name='student register'),
    url(r'^teacher_register/', teacher_register, name='teacher register'),
    url(r'^home_page/', student_home, name='home page'),
    url(r'^test/', test_questions, name='test questions'),
    url(r'^index_page/', home_page, name='index page'),
    url(r'^student_videos/', student_videos, name='student videos'),
    url(r'^student_results/', student_results, name='student results'),
    url(r'^store_test_data/', StoreTestData, name='Test Data'),
    url(r'^results/', StudentResultsView, name='Student Results View'),
    url(r'^all_results/', TeacherResultsView, name='Teacher Results View'),
    url(r'^student_profile/', Student_Profile, name='Student Profile View'),
    url(r'^teacher_profile/', Teacher_Profile, name='Teacher Profile View'),
    url(r'^contact_us/', contact_us, name='Contact Us'),
    url(r'^about_us/', about_us, name='About Us'),
    url(r'^stu_profile_update/', student_profile_update, name='student profile update'),
    url(r'^teacher_profile_update/', teacher_profile_update, name='teacher profile update'),
    url(r'^upload_video/', post_video, name='upload video'),
    url(r'^student_videos_view/', get_videos, name='display videos'),
    url(r'^logout/', Logout, name='Logout')
]
