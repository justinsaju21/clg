from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        TEACHER = 'TEACHER', _('Teacher')
        TA = 'TA', _('Teaching Assistant')
        ADMIN = 'ADMIN', _('Administrator')

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    reg_no = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Registration Number for Students/Faculty")
    department = models.CharField(max_length=100, default="ECE")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=3)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': User.Roles.TEACHER}, related_name='courses_taught')
    cover_image = models.ImageField(upload_to='course_covers/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    gamification_mode = models.BooleanField(default=False, help_text="Enable game-like features such as unlocking levels.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.name}"

class Syllabus(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='syllabus')
    content = models.TextField(help_text="Markdown supported course objectives and outline.")
    
    def __str__(self):
        return f"Syllabus for {self.course.name}"

class GradingWeight(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name='weights')
    category_name = models.CharField(max_length=50) # e.g. "Quizzes", "Assignments"
    percentage = models.PositiveIntegerField(help_text="Weight percentage (e.g. 20 for 20%)")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['syllabus', 'category_name'], name='unique_weight_category')
        ]
