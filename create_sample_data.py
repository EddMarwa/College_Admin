#!/usr/bin/env python
"""
Django script to create sample users for testing different user roles
"""

import os
import django
import sys

# Add the project directory to Python path
sys.path.append(r'c:\Users\EDDX\Desktop\CollegeManagement-Django')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management_system.settings')
django.setup()

from main_app.models import CustomUser, Course, Session, Subject, Staff, Student
from django.contrib.auth.hashers import make_password
from datetime import date

def create_sample_data():
    print("Creating sample data...")
    
    # Create a course
    course, created = Course.objects.get_or_create(
        name="Computer Science",
        defaults={'name': "Computer Science"}
    )
    if created:
        print("✓ Created Computer Science course")
    else:
        print("✓ Computer Science course already exists")
    
    # Create a session
    session, created = Session.objects.get_or_create(
        start_year=date(2024, 9, 1),
        end_year=date(2025, 6, 30),
        defaults={
            'start_year': date(2024, 9, 1),
            'end_year': date(2025, 6, 30)
        }
    )
    if created:
        print("✓ Created 2024-2025 academic session")
    else:
        print("✓ 2024-2025 academic session already exists")
    
    # Create a staff user
    staff_email = "staff@college.com"
    if not CustomUser.objects.filter(email=staff_email).exists():
        staff_user = CustomUser.objects.create(
            email=staff_email,
            first_name="John",
            last_name="Teacher",
            user_type="2",  # Staff
            gender="M",
            address="123 Faculty Street, College Town",
            password=make_password("staff123")
        )
        
        # The staff profile is created automatically via signals
        staff_profile = Staff.objects.get(admin=staff_user)
        staff_profile.course = course
        staff_profile.save()
        
        print(f"✓ Created staff user: {staff_email} / staff123")
    else:
        print(f"✓ Staff user already exists: {staff_email}")
    
    # Create a subject
    staff_user = CustomUser.objects.get(email=staff_email)
    staff_profile = Staff.objects.get(admin=staff_user)
    
    subject, created = Subject.objects.get_or_create(
        name="Python Programming",
        defaults={
            'name': "Python Programming",
            'staff': staff_profile,
            'course': course
        }
    )
    if created:
        print("✓ Created Python Programming subject")
    else:
        print("✓ Python Programming subject already exists")
    
    # Create a student user
    student_email = "student@college.com"
    if not CustomUser.objects.filter(email=student_email).exists():
        student_user = CustomUser.objects.create(
            email=student_email,
            first_name="Jane",
            last_name="Student",
            user_type="3",  # Student
            gender="F",
            address="456 Student Avenue, College Town",
            password=make_password("student123")
        )
        
        # The student profile is created automatically via signals
        student_profile = Student.objects.get(admin=student_user)
        student_profile.course = course
        student_profile.session = session
        student_profile.save()
        
        print(f"✓ Created student user: {student_email} / student123")
    else:
        print(f"✓ Student user already exists: {student_email}")
    
    print("\n🎉 Sample data creation complete!")
    print("\nLogin credentials:")
    print("Admin (HOD): admin@admin.com / [your admin password]")
    print("Staff: staff@college.com / staff123")
    print("Student: student@college.com / student123")

if __name__ == "__main__":
    create_sample_data()
