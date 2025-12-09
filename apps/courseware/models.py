from django.db import models
from polymorphic.models import PolymorphicModel
from apps.core.models import Course

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.course_code} - {self.title}"

class Unit(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"

class LearningActivity(PolymorphicModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    # Gamification / Breakthrough Mode
    previous_activity_required = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='unlocks_next')
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.get_real_instance_class().__name__})"

class VideoResource(LearningActivity):
    video_url = models.URLField(help_text="Link to video file or stream")
    duration_minutes = models.PositiveIntegerField(default=0)

class PDFResource(LearningActivity):
    file = models.FileField(upload_to='course_pdfs/')
    
class Assignment(LearningActivity):
    due_date = models.DateTimeField()
    max_points = models.PositiveIntegerField(default=100)
    allow_file_upload = models.BooleanField(default=True)
    allow_code_editor = models.BooleanField(default=False, help_text="Enable Monaco Editor for Verilog/C")

class Quiz(LearningActivity):
    time_limit_minutes = models.PositiveIntegerField(default=30)
    pass_score = models.PositiveIntegerField(default=60)

class Discussion(LearningActivity):
    topic = models.CharField(max_length=255)
