from django.urls import path
from . import views, demo_views

app_name = 'courseware'

urlpatterns = [
    path('<str:course_code>/', views.CourseDetailView.as_view(), name='course_home'),
    path('<str:course_code>/syllabus/', views.course_syllabus, name='course_syllabus'),
    path('<str:course_code>/content/', views.course_courseware, name='course_tree'),
    path('<str:course_code>/activity/<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('demo-unlock/<int:activity_id>/', demo_views.demo_unlock, name='demo_unlock'),
]
