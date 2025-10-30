import os
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import transaction
from faker import Faker
from users.models import User, JobSeeker, Employer
from skills.models import Skill
from resumes.models import Resume
from notifications.models import Notification
from jobs.models import Job, Location, Category
from applications.models import Application
from analytics.models import Analytics

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)'
        )
        parser.add_argument(
            '--jobs',
            type=int,
            default=30,
            help='Number of jobs to create (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating'
        )

    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write("Clearing existing data...")
            self.clear_existing_data()
        
        self.stdout.write("Creating dummy data...")

        # Create locations
        locations = self.create_locations(fake)
        
        # Create categories
        categories = self.create_categories(fake)
        
        # Create users with different roles
        users_count = options['users']
        job_seekers_count = int(users_count * 0.7)  # 70% job seekers
        employers_count = int(users_count * 0.25)   # 25% employers
        admins_count = users_count - job_seekers_count - employers_count  # 5% admins

        # Create job seekers
        job_seekers = self.create_job_seekers(fake, job_seekers_count)
        
        # Create employers
        employers = self.create_employers(fake, employers_count)
        
        # Create admin users
        self.create_admins(fake, admins_count)
        
        # Create skills for job seekers
        self.create_skills(fake, job_seekers)
        
        # Create resumes for job seekers
        self.create_resumes_simple(fake, job_seekers)
        
        # Create jobs
        jobs_count = options['jobs']
        jobs = self.create_jobs(fake, jobs_count, employers, locations, categories)
        
        # Create applications
        self.create_applications(fake, job_seekers, jobs)
        
        # Create notifications
        all_users = []
        for job_seeker in job_seekers:
            all_users.append(job_seeker.user)
        for employer in employers:
            all_users.append(employer.user)
        self.create_notifications(fake, all_users)
        
        # Create analytics (SIMPLIFIED: Only create one record per job)
        self.create_analytics_simple(jobs)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated database with:\n"
                f"- {User.objects.count()} users\n"
                f"- {JobSeeker.objects.count()} job seekers\n"
                f"- {Employer.objects.count()} employers\n"
                f"- {Skill.objects.count()} skills\n"
                f"- {Resume.objects.count()} resumes\n"
                f"- {Job.objects.count()} jobs\n"
                f"- {Application.objects.count()} applications\n"
                f"- {Notification.objects.count()} notifications\n"
                f"- {Analytics.objects.count()} analytics records"
            )
        )

    def clear_existing_data(self):
        """Clear all existing data from the database"""
        # Delete in reverse order to respect foreign key constraints
        Analytics.objects.all().delete()
        Application.objects.all().delete()
        Notification.objects.all().delete()
        Resume.objects.all().delete()
        Skill.objects.all().delete()
        Job.objects.all().delete()
        Location.objects.all().delete()
        Category.objects.all().delete()
        JobSeeker.objects.all().delete()
        Employer.objects.all().delete()
        User.objects.all().delete()
        
        self.stdout.write("All existing data cleared successfully")

    def create_locations(self, fake):
        locations = []
        cities = ['New York', 'San Francisco', 'Chicago', 'Austin', 'Seattle', 
                 'Boston', 'Denver', 'Los Angeles', 'Miami', 'Atlanta']
        
        for city in cities:
            location, created = Location.objects.get_or_create(
                city=city,
                defaults={
                    'state': fake.state(),
                    'country': 'USA'
                }
            )
            locations.append(location)
        
        self.stdout.write(f"Created/retrieved {len(locations)} locations")
        return locations

    def create_categories(self, fake):
        categories_data = [
            ('Software Development', 'Jobs related to software engineering and development'),
            ('Data Science', 'Jobs in data analysis, machine learning, and AI'),
            ('Marketing', 'Marketing and advertising positions'),
            ('Sales', 'Sales and business development roles'),
            ('Design', 'UI/UX design and graphic design positions'),
            ('Finance', 'Financial analysis and accounting jobs'),
            ('Healthcare', 'Medical and healthcare positions'),
            ('Education', 'Teaching and educational roles'),
            ('Operations', 'Business operations and management'),
            ('Customer Support', 'Customer service and support roles'),
        ]
        
        categories = []
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            categories.append(category)
        
        self.stdout.write(f"Created/retrieved {len(categories)} categories")
        return categories

    def create_job_seekers(self, fake, count):
        job_seekers = []
        for i in range(count):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password='password123',
                role='job_seeker'
            )
            
            job_seeker = JobSeeker.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15]
            )
            job_seekers.append(job_seeker)
            
            if i % 10 == 0:
                self.stdout.write(f"Created {i+1} job seekers...")
        
        self.stdout.write(f"Created {len(job_seekers)} job seekers")
        return job_seekers

    def create_employers(self, fake, count):
        employers = []
        company_types = ['Tech', 'Solutions', 'Systems', 'Group', 'Labs', 'Ventures', 'Corp']
        
        for i in range(count):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password='password123',
                role='employer'
            )
            
            company_name = f"{fake.company()} {random.choice(company_types)}"
            employer = Employer.objects.create(
                user=user,
                company_name=company_name,
                company_description=fake.paragraph(nb_sentences=3),
                website=fake.url()
            )
            employers.append(employer)
            
            if i % 5 == 0:
                self.stdout.write(f"Created {i+1} employers...")
        
        self.stdout.write(f"Created {len(employers)} employers")
        return employers

    def create_admins(self, fake, count):
        for i in range(count):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password='admin123',
                role='admin'
            )
            
            if i == 0:
                self.stdout.write(f"Created admin user: {email}")

    def create_skills(self, fake, job_seekers):
        skills_list = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Django', 'Flask',
            'Node.js', 'SQL', 'MongoDB', 'AWS', 'Docker', 'Kubernetes', 'Git',
            'Machine Learning', 'Data Analysis', 'UI/UX Design', 'Project Management',
            'Agile Methodology', 'DevOps', 'Cybersecurity', 'Cloud Computing',
            'TensorFlow', 'PyTorch', 'Swift', 'Kotlin', 'TypeScript', 'Angular',
            'Vue.js', 'Spring Boot', 'Ruby on Rails', 'PHP', 'WordPress'
        ]
        
        for job_seeker in job_seekers:
            num_skills = random.randint(3, 8)
            user_skills = random.sample(skills_list, num_skills)
            
            for skill_name in user_skills:
                Skill.objects.create(
                    name=skill_name,
                    user=job_seeker.user
                )
        
        self.stdout.write(f"Created skills for {len(job_seekers)} job seekers")

    def create_resumes_simple(self, fake, job_seekers):
        """Create resume records without file uploads to avoid checksum issues"""
        for job_seeker in job_seekers:
            try:
                # Create a simple text file with unique content
                resume_content = f"""
RESUME FOR {job_seeker.first_name} {job_seeker.last_name}
Email: {job_seeker.user.email}
Phone: {job_seeker.phone_number if job_seeker.phone_number else 'N/A'}

PROFESSIONAL SUMMARY
Experienced professional with a background in technology and development.

UNIQUE IDENTIFIER: {fake.uuid4()}
TIMESTAMP: {datetime.now().isoformat()}
RANDOM: {random.randint(100000, 999999)}
                """.strip()
                
                filename = f"resume_{job_seeker.user.email}_{fake.uuid4()}.txt"
                file_content = ContentFile(resume_content.encode('utf-8'))
                
                # Create and save resume
                resume = Resume(job_seeker=job_seeker)
                resume.file_path.save(filename, file_content)
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Failed to create resume for {job_seeker}: {str(e)}")
                )
                # Create resume without file as fallback
                try:
                    resume = Resume.objects.create(job_seeker=job_seeker)
                    # Manually set a unique checksum
                    resume.checksum = f"dummy_checksum_{job_seeker.user.email}_{fake.uuid4()}"
                    resume.save(update_fields=['checksum'])
                except Exception as e2:
                    self.stdout.write(
                        self.style.ERROR(f"Completely failed to create resume for {job_seeker}: {str(e2)}")
                    )
                continue
        
        self.stdout.write(f"Created resumes for {len(job_seekers)} job seekers")

    def create_jobs(self, fake, count, employers, locations, categories):
        job_titles = [
            'Senior Software Engineer', 'Frontend Developer', 'Backend Developer',
            'Full Stack Developer', 'Data Scientist', 'DevOps Engineer',
            'Product Manager', 'UX Designer', 'Data Analyst', 'Systems Administrator',
            'Cloud Architect', 'Mobile Developer', 'QA Engineer', 'Security Analyst',
            'Database Administrator', 'Technical Lead', 'Scrum Master', 'Business Analyst'
        ]
        
        jobs = []
        for i in range(count):
            # Use timezone-aware datetime to avoid warnings
            expires_at = timezone.now() + timedelta(days=random.randint(30, 90))
            
            job = Job.objects.create(
                employer=random.choice(employers),
                title=random.choice(job_titles),
                description=fake.paragraph(nb_sentences=8),
                location=random.choice(locations),
                category=random.choice(categories),
                salary_range=f"${random.randint(60, 150)}k - ${random.randint(151, 250)}k",
                job_type=random.choice(['full-time', 'part-time', 'remote']),
                expires_at=expires_at,
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            jobs.append(job)
            
            if i % 10 == 0:
                self.stdout.write(f"Created {i+1} jobs...")
        
        self.stdout.write(f"Created {len(jobs)} jobs")
        return jobs

    def create_applications(self, fake, job_seekers, jobs):
        applications_created = 0
        for job in jobs:
            # Each job gets 2-8 applications
            num_applications = random.randint(2, 8)
            applicants = random.sample(job_seekers, min(num_applications, len(job_seekers)))
            
            for applicant in applicants:
                # Get applicant's resume
                resumes = applicant.resumes.all()
                if resumes.exists():
                    resume = resumes.first()
                    
                    try:
                        application = Application.objects.create(
                            job_seeker=applicant,
                            job=job,
                            resume=resume,
                            cover_letter=fake.paragraph(nb_sentences=4),
                            status=random.choice(['pending', 'reviewed', 'rejected', 'accepted'])
                        )
                        applications_created += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f"Failed to create application: {str(e)}")
                        )
                        continue
        
        self.stdout.write(f"Created {applications_created} applications")

    def create_notifications(self, fake, users):
        """Create notifications for users"""
        notifications_created = 0
        for user in users:
            num_notifications = random.randint(1, 5)
            for _ in range(num_notifications):
                try:
                    Notification.objects.create(
                        user=user,
                        message=fake.sentence(),
                        is_read=random.choice([True, False])
                    )
                    notifications_created += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to create notification for user {user.email}: {str(e)}")
                    )
                    continue
        
        self.stdout.write(f"Created {notifications_created} notifications for {len(users)} users")

    def create_analytics_simple(self, jobs):
        """Create simple analytics records - one per job for today only"""
        analytics_created = 0
        
        for job in jobs:
            try:
                # Create only one analytics record per job for today
                analytics = Analytics.objects.create(
                    job=job,
                    date=timezone.now().date(),
                    views=random.randint(0, 50),
                    applications=random.randint(0, 10),
                )
                analytics_created += 1
                        
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Failed to create analytics for job {job.title}: {str(e)}")
                )
                continue
        
        self.stdout.write(f"Created {analytics_created} analytics records for {len(jobs)} jobs")