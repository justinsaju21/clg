from django.db import models
from apps.core.models import User
from apps.courseware.models import Assignment, Quiz

class RubricCriteria(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='rubrics')
    criteria_name = models.CharField(max_length=100)
    max_score = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.criteria_name} ({self.max_score} pts)"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='submissions/', blank=True, null=True)
    code_content = models.TextField(blank=True, help_text="Verilog/C code from Monaco Editor")
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"

class GroupSubmission(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='group_info')
    members = models.ManyToManyField(User, related_name='group_submissions')
    
    def __str__(self):
        return f"Group Submission for {self.submission.assignment.title}"

# Quiz Models

class QuestionBank(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'SINGLE', 'Single Choice'
        MULTI_CHOICE = 'MULTI', 'Multiple Choice'
        CODING = 'CODING', 'Coding Challenge'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    points = models.PositiveIntegerField(default=1)
    
    # For coding questions
    code_template = models.TextField(blank=True, help_text="Starter code")
    test_cases = models.TextField(blank=True, help_text="JSON or script for validation")

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.text[:50]}..."

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} attempt at {self.quiz.title}"

class Answer(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
