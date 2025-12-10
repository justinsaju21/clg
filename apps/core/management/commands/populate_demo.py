from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.core.models import User, Course, Syllabus
from apps.courseware.models import Chapter, Unit, VideoResource, PDFResource, Assignment
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
        course_soc, _ = Course.objects.get_or_create(course_code='IICD504', defaults={
            'name': 'SYSTEM-ON-CHIP TESTING',
            'instructor': instructor,
            'credits': 4,
            'is_public': True,
            'gamification_mode': False
        })
        
        # Ensure Syllabus
        Syllabus.objects.get_or_create(course=course_soc, defaults={'content': "# Objectives\nMaster SoC testing methodologies."})

        # CH1: Overview
        ch_over, _ = Chapter.objects.get_or_create(course=course_soc, title="00_overview", defaults={'order': 1})
        u_over, _ = Unit.objects.get_or_create(chapter=ch_over, title="00_overview", defaults={'order': 1})
        VideoResource.objects.get_or_create(unit=u_over, title="Overview Video", defaults={'video_url': "https://www.youtube.com/watch?v=gI-qXk7XojA", 'duration_minutes': 10, 'order': 1})

        # CH2: Introduction
        ch_intro, _ = Chapter.objects.get_or_create(course=course_soc, title="01_Introduction", defaults={'order': 2})
        u_intro, _ = Unit.objects.get_or_create(chapter=ch_intro, title="01_Introduction", defaults={'order': 1})
        VideoResource.objects.get_or_create(unit=u_intro, title="Intro Video", defaults={'video_url': "https://www.youtube.com/watch?v=gI-qXk7XojA", 'duration_minutes': 15, 'order': 1})
        PDFResource.objects.get_or_create(unit=u_intro, title="[NSYSU/SRM]CH1 Mind map Finished", defaults={'file': "demo.pdf", 'order': 2})

        # CH3: Fault Model
        ch_fault, _ = Chapter.objects.get_or_create(course=course_soc, title="02_Fault model", defaults={'order': 3})
        u_fault, _ = Unit.objects.get_or_create(chapter=ch_fault, title="Fault Models", defaults={'order': 1})
        PDFResource.objects.get_or_create(unit=u_fault, title="Stuck-at Faults Readings", defaults={'file': "faults.pdf", 'order': 1})


        # ==========================================
        # Course 2: Digital Logic Design
        # ==========================================
        course_dld, _ = Course.objects.get_or_create(course_code='ECE-201', defaults={
            'name': 'Digital Logic Design',
            'instructor': instructor,
            'credits': 3,
            'is_public': True,
            'gamification_mode': False
        })

        Syllabus.objects.get_or_create(course=course_dld, defaults={'content': "# Objectives\nDesign complex digital systems."})
        
        ch1, _ = Chapter.objects.get_or_create(course=course_dld, title="Number Systems", defaults={'order': 1})
        u1, _ = Unit.objects.get_or_create(chapter=ch1, title="Binary & Hex", defaults={'order': 1})
        VideoResource.objects.get_or_create(unit=u1, title="Binary Arithmetic", defaults={'video_url': "https://www.youtube.com/watch?v=gI-qXk7XojA", 'duration_minutes': 12, 'order': 1})
        
        ch2, _ = Chapter.objects.get_or_create(course=course_dld, title="K-Maps", defaults={'order': 2})
        u2, _ = Unit.objects.get_or_create(chapter=ch2, title="Simplification", defaults={'order': 1})
        
        # Assignment needs unique title per unit
        if not Assignment.objects.filter(unit=u2, title="K-Map Homework 1").exists():
            Assignment.objects.create(unit=u2, title="K-Map Homework 1", due_date=timezone.now() + datetime.timedelta(days=5), order=1)

        # ==========================================
        # Course 3: VLSI Design and Technology
        # ==========================================
        course_vlsi, _ = Course.objects.get_or_create(course_code='ECE-405', defaults={
            'name': 'VLSI Design and Technology',
            'instructor': instructor,
            'credits': 4,
            'is_public': True,
            'gamification_mode': False
        })

        Syllabus.objects.get_or_create(course=course_vlsi, defaults={'content': "# Objectives\nCMOS Transistor theory."})
        
        ch_mos, _ = Chapter.objects.get_or_create(course=course_vlsi, title="MOSFET Theory", defaults={'order': 1})
        u_mos, _ = Unit.objects.get_or_create(chapter=ch_mos, title="IV Characteristics", defaults={'order': 1})
        PDFResource.objects.get_or_create(unit=u_mos, title="MOSFET Equations", defaults={'file': "idvg.pdf", 'order': 1})
        
        ch_fab, _ = Chapter.objects.get_or_create(course=course_vlsi, title="Fabrication Process", defaults={'order': 2})
        u_fab, _ = Unit.objects.get_or_create(chapter=ch_fab, title="Lithography", defaults={'order': 1})
        VideoResource.objects.get_or_create(unit=u_fab, title="Photolithography Steps", defaults={'video_url': "https://www.youtube.com/watch?v=gI-qXk7XojA", 'duration_minutes': 20, 'order': 1})

        self.stdout.write(self.style.SUCCESS('Successfully populated New Demo Courses (Idempotent)!'))
