from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .models import Course, User

@login_required
def dashboard(request):
    """
    The 'My Home' Dashboard view.
    Layout: 3 Columns.
    """
    user = request.user

    # Self-Healing: If courses are missing, run the population script
    # We check specifically for our demo course code to avoid false positives
    if not Course.objects.filter(course_code='IICD504').exists():
        try:
            print("Auto-populating demo content...")
            call_command('populate_demo')
        except Exception as e:
            print(f"Error auto-populating: {e}")
    
    # Context data
    context = {
        'student': user,
        # Ensure we grab ALL courses to display
        'courses': Course.objects.all(), 
        'todo_list': [
            {'title': 'HW5: Verilog Adder', 'due': '2025-12-11', 'status': 'urgent'},
            {'title': 'Quiz 3: CMOS Logic', 'due': '2025-12-12', 'status': 'normal'},
        ],
        'announcements': [
            {'title': 'Online Teaching Survey', 'date': '2025-12-09', 'author': 'Admin'},
            {'title': 'Lab 4 Grades Released', 'date': '2025-12-08', 'author': 'TA'},
        ],
        'radar_data': [80, 65, 90, 75, 100], 
    }
    return render(request, 'core/dashboard.html', context)
