from django.shortcuts import render, get_object_or_404
from apps.courseware.models import LearningActivity

class BreakthroughModeMiddleware:
    """
    Middleware to check if a student has completed the previous activity 
    before accessing the current one.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Only check on activity detail views
        if 'activity_id' not in view_kwargs:
            return None
        
        try:
            activity = LearningActivity.objects.get(id=view_kwargs['activity_id'])
        except LearningActivity.DoesNotExist:
            return None

        # Check if activity requires a previous one
        if activity.previous_activity_required:
            previous_activity = activity.previous_activity_required
            
            # MOCK LOGIC FOR DEMO:
            # Check if there is a 'completion' record for the previous activity.
            # In a real app, you'd have a StudentActivityCompletion model.
            # For this MVP demo, let's assume if the USER is a 'Student' and 
            # the previous activity ID is not in their session 'completed_ids', it's locked.
            # We'll toggle completion via a secret or just checking a mock list.
            
            # For the demo, let's just Block EVERYTHING if it has a prerequisite
            # unless we specifically 'unlock' it.
            
            # Let's check for a session variable 'completed_activities'
            completed_ids = request.session.get('completed_ids', [])
            
            if previous_activity.id not in completed_ids:
                # Render the specific "Access Denied" demo page
                return render(request, 'courseware/access_denied.html', {
                    'locked_activity': activity,
                    'prerequisite': previous_activity
                })
        
        return None
