from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('generate/<str:course_code>/', views.generate_code, name='generate_code'),
    path('submit/<str:course_code>/', views.submit_attendance, name='submit_attendance'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('my-attendance/<str:course_code>/', views.student_attendance_view, name='student_view'),
]
