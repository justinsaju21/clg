from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course, User

@login_required
def dashboard(request):
    """
    The 'My Home' Dashboard view.
    Layout: 3 Columns.
    1. Left: Learning Status (Radar Chart) + User Profile.
    2. Center: My Courses List.
    3. Right: To-Do List & Announcements.
    """
    user = request.user
    
    # Context data (Mocked for now mostly, but using models where possible)
    context = {
        'student': user,
        'courses': Course.objects.filter(is_public=True), # Placeholder query
        'todo_list': [
            {'title': 'HW5: Verilog Adder', 'due': '2025-12-11', 'status': 'urgent'},
            {'title': 'Quiz 3: CMOS Logic', 'due': '2025-12-12', 'status': 'normal'},
        ],
        'announcements': [
            {'title': 'Online Teaching Survey', 'date': '2025-12-09', 'author': 'Admin'},
            {'title': 'Lab 4 Grades Released', 'date': '2025-12-08', 'author': 'TA'},
        ],
        # Chart Data (Passed as JSON safe structure usually, simplified here)
        'radar_data': [80, 65, 90, 75, 100], # Video, Quiz, Discussion, Assignment, Attendance
    }
    return render(request, 'core/dashboard.html', context)
