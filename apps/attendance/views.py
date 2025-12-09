from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib import messages
from apps.core.models import Course, User
from .models import AttendanceSession, AttendanceRecord

def is_teacher(user):
    return user.role == User.Roles.TEACHER or user.is_staff

@login_required
@user_passes_test(is_teacher)
def generate_code(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    
    # Generate 4-digit code
    code = get_random_string(length=4, allowed_chars='0123456789')
    
    session = AttendanceSession.objects.create(
        course=course,
        code=code,
        duration_minutes=5 # Valid for 5 mins
    )
    
    messages.success(request, f"Attendance Code Generated: {code}")
    return redirect('attendance:session_detail', session_id=session.id)

@login_required
def submit_attendance(request, course_code):
    if request.method == 'POST':
        code = request.POST.get('code')
        course = get_object_or_404(Course, course_code=course_code)
        
        # Find active session
        now = timezone.now()
        # Naive filtering for active sessions
        # In prod: use created_at__gte=now-timedelta
        
        sessions = AttendanceSession.objects.filter(course=course, code=code, is_active=True)
        valid_session = None
        
        for s in sessions:
            if s.is_valid():
                valid_session = s
                break
        
        if valid_session:
            AttendanceRecord.objects.get_or_create(
                session=valid_session,
                student=request.user,
                defaults={'status': AttendanceRecord.Status.PRESENT}
            )
            messages.success(request, "Attendance Marked Successfully!")
        else:
            messages.error(request, "Invalid or Expired Code.")
            
    return redirect('courseware:course_home', course_code=course_code)

@login_required
@user_passes_test(is_teacher)
def session_detail(request, session_id):
    session = get_object_or_404(AttendanceSession, id=session_id)
    return render(request, 'attendance/session_detail.html', {'session': session})

@login_required
def student_attendance_view(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    # Aggregate stats logic here
    return render(request, 'attendance/student_view.html', {'course': course})
