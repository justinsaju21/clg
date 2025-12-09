from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.models import Course
from .models import Chapter, LearningActivity

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courseware/course_home.html'
    context_object_name = 'course'
    
    def get_object(self):
        return get_object_or_404(Course, course_code=self.kwargs['course_code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mocking active tab for sidebar highlighting
        context['active_tab'] = 'home'
        return context

@login_required
def course_syllabus(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)
    return render(request, 'courseware/course_syllabus.html', {
        'course': course,
        'active_tab': 'syllabus'
    })

@login_required
def course_courseware(request, course_code):
    """
    Renders the Courseware Tree: Chapters -> Units -> Activities.
    """
    course = get_object_or_404(Course, course_code=course_code)
    chapters = course.chapters.prefetch_related('units__activities').all()
    
    return render(request, 'courseware/course_tree.html', {
        'course': course,
        'chapters': chapters,
        'active_tab': 'courseware'
    })

@login_required
def activity_detail(request, course_code, activity_id):
    course = get_object_or_404(Course, course_code=course_code)
    activity = get_object_or_404(LearningActivity, id=activity_id)
    
    # Breakthrough logic check would go here (Part 3)
    
    return render(request, 'courseware/activity_detail.html', {
        'course': course,
        'activity': activity,
        'active_tab': 'courseware' # Stay on courseware tab
    })
