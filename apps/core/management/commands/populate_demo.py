from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import User, Course, Syllabus, GradingWeight
from apps.courseware.models import Chapter, Unit, VideoResource, PDFResource, Assignment, Quiz, Discussion

class Command(BaseCommand):
    help = 'Populate the database with a full demo Physics/Logic course'

    def handle(self, *args, **options):
        self.stdout.write("Starting Demo Population...")

        # 1. Get or Create Instructor
        instructor, _ = User.objects.get_or_create(username='dr_strange', defaults={
            'email': 'range@example.com',
            'first_name': 'Stephen',
            'last_name': 'Strange',
            'role': User.Roles.TEACHER,
            'department': 'Physics'
        })
        if not instructor.check_password('magic'):
            instructor.set_password('magic')
            instructor.save()

        # 2. Create Course
        course, created = Course.objects.get_or_create(course_code='ECE-101', defaults={
            'name': 'Introduction to Digital Logic',
            'instructor': instructor,
            'credits': 4,
            'is_public': True,
            'gamification_mode': True
        })
        
        if not created:
            self.stdout.write("Course already exists. Skipping...")
            return

        # 3. Create Syllabus
        syllabus = Syllabus.objects.create(course=course, content="""
# Course Objectives
1. Understand boolean algebra.
2. Master logic gates.
3. Design sequential circuits.

# Grading
- Quizzes: 30%
- Labs: 40%
- Final: 30%
        """)

        # 4. Create Chapters & Units (The Fun Part)
        
        # --- Chapter 1: Foundations ---
        ch1 = Chapter.objects.create(course=course, title="Boolean Algebra", order=1)
        
        # Unit 1.1: Basics
        u1 = Unit.objects.create(chapter=ch1, title="Logic Gates 101", order=1)
        
        # Activity 1: Video (Unlocked)
        vid1 = VideoResource.objects.create(
            unit=u1,
            title="Intro to AND/OR/NOT",
            description="Watch this 5 minute primer on basic gates.",
            order=1,
            video_url="https://www.youtube.com/watch?v=gI-qXk7XojA", # Valid youtube link
            duration_minutes=5
        )

        # Activity 2: PDF Reading (Unlocked)
        pdf1 = PDFResource.objects.create(
            unit=u1,
            title="Truth Tables Cheatsheet",
            description="Download this reference guide.",
            order=2,
            previous_activity_required=None # No requirement yet
        )

        # Activity 3: Quiz (LOCKED by Video)
        # In a real app, completing Vid1 unlocks this. 
        # For now, we set the dependency to demonstrate the "Lock" UI.
        quiz1 = Quiz.objects.create(
            unit=u1,
            title="Gate Logic Check",
            description="Test your knowledge of AND gates.",
            order=3,
            previous_activity_required=vid1, # <--- LOCK!
            pass_score=80
        )

        # --- Chapter 2: Combinational Logic ---
        ch2 = Chapter.objects.create(course=course, title="Combinational Circuits", order=2)
        u2 = Unit.objects.create(chapter=ch2, title="adders & Subtractors", order=1)
        
        assign1 = Assignment.objects.create(
            unit=u2,
            title="Design a Full Adder",
            description="Submit your Verilog code for a 1-bit full adder.",
            order=1,
            due_date=timezone.now() + timezone.timedelta(days=7),
            allow_code_editor=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated ECE-101 Demo Course!'))
