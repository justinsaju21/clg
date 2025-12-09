from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

@require_POST
def demo_unlock(request, activity_id):
    """
    Helper view for the Demo: Marks an activity as 'complete' in the session
    so the presenter can show the Breakthrough unlocking.
    """
    completed = request.session.get('completed_ids', [])
    if activity_id not in completed:
        completed.append(activity_id)
        request.session['completed_ids'] = completed
        messages.success(request, "Activity marked as distinct completed! (Demo Mode)")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
