from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import User, Course, Syllabus, GradingWeight
from apps.courseware.models import Chapter, Unit, VideoResource, PDFResource, Assignment, Quiz, Discussion
import datetime

class Command(BaseCommand):
    help = 'Populate the database with System-on-Chip, Digital Logic, and VLSI Design courses'

    def handle(self, *args, **options):
        self.stdout.write("Starting Demo Population...")

        # 1. Get or Create Instructor
        instructor, _ = User.objects.get_or_create(username='prof_xavier', defaults={
            'email': 'x@example.com',
            'first_name': 'Charles',
            'last_name': 'Xavier',
            'role': User.Roles.TEACHER,
            'department': 'Electronics'
        })
        if not instructor.check_password('cerebro'):
            instructor.set_password('cerebro')
            instructor.save()

        # ==========================================
        # Course 1: System-on-Chip Testing
        # ==========================================
        course_soc, created = Course.objects.get_or_create(course_code='IICD504', defaults={
            'name': 'SYSTEM-ON-CHIP TESTING',
            'instructor': instructor,
            'credits': 4,
            'is_public': True,
            'gamification_mode': False # Disabled as per request
        })
        
        if created:
             # Syllabus
            Syllabus.objects.create(course=course_soc, content="# Objectives\nMaster SoC testing methodologies.")

            # Chapter 1: Overview
            ch_over = Chapter.objects.create(course=course_soc, title="00_overview", order=1)
            u_over = Unit.objects.create(chapter=ch_over, title="00_overview", order=1)
            VideoResource.objects.create(unit=u_over, title="Overview Video", video_url="https://www.youtube.com/watch?v=gI-qXk7XojA", duration_minutes=10, order=1)

            # Chapter 2: Introduction
            ch_intro = Chapter.objects.create(course=course_soc, title="01_Introduction", order=2)
            u_intro = Unit.objects.create(chapter=ch_intro, title="01_Introduction", order=1)
            VideoResource.objects.create(unit=u_intro, title="Intro Video", video_url="https://www.youtube.com/watch?v=gI-qXk7XojA", duration_minutes=15, order=1)
            PDFResource.objects.create(unit=u_intro, title="[NSYSU/SRM]CH1 Mind map Finished", file="demo.pdf", order=2)

            # Chapter 3: Fault Model
            ch_fault = Chapter.objects.create(course=course_soc, title="02_Fault model", order=3)
            u_fault = Unit.objects.create(chapter=ch_fault, title="Fault Models", order=1)
            PDFResource.objects.create(unit=u_fault, title="Stuck-at Faults Readings", file="faults.pdf", order=1)

        # ==========================================
        # Course 2: Digital Logic Design
        # ==========================================
        course_dld, created = Course.objects.get_or_create(course_code='ECE-201', defaults={
            'name': 'Digital Logic Design',
            'instructor': instructor,
            'credits': 3,
            'is_public': True,
            'gamification_mode': False
        })

        if created:
            Syllabus.objects.create(course=course_dld, content="# Objectives\nDesign complex digital systems.")
            
            ch1 = Chapter.objects.create(course=course_dld, title="Number Systems", order=1)
            u1 = Unit.objects.create(chapter=ch1, title="Binary & Hex", order=1)
            VideoResource.objects.create(unit=u1, title="Binary Arithmetic", video_url="https://www.youtube.com/watch?v=gI-qXk7XojA", duration_minutes=12, order=1)
            
            ch2 = Chapter.objects.create(course=course_dld, title="K-Maps", order=2)
            u2 = Unit.objects.create(chapter=ch2, title="Simplification", order=1)
            Assignment.objects.create(unit=u2, title="K-Map Homework 1", due_date=datetime.datetime.now() + datetime.timedelta(days=5), order=1)

        # ==========================================
        # Course 3: VLSI Design and Technology
        # ==========================================
        course_vlsi, created = Course.objects.get_or_create(course_code='ECE-405', defaults={
            'name': 'VLSI Design and Technology',
            'instructor': instructor,
            'credits': 4,
            'is_public': True,
            'gamification_mode': False
        })

        if created:
            Syllabus.objects.create(course=course_vlsi, content="# Objectives\nCMOS Transistor theory.")
            
            ch_mos = Chapter.objects.create(course=course_vlsi, title="MOSFET Theory", order=1)
            u_mos = Unit.objects.create(chapter=ch_mos, title="IV Characteristics", order=1)
            PDFResource.objects.create(unit=u_mos, title="MOSFET Equations", file="idvg.pdf", order=1)
            
            ch_fab = Chapter.objects.create(course=course_vlsi, title="Fabrication Process", order=2)
            u_fab = Unit.objects.create(chapter=ch_fab, title="Lithography", order=1)
            VideoResource.objects.create(unit=u_fab, title="Photolithography Steps", video_url="https://www.youtube.com/watch?v=gI-qXk7XojA", duration_minutes=20, order=1)

        self.stdout.write(self.style.SUCCESS('Successfully populated New Demo Courses!'))
