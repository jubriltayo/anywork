import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from faker import Faker

from users.models import User, JobSeeker, Employer
from skills.models import Skill
from resumes.models import Resume
from notifications.models import Notification
from jobs.models import Job, Location, Category
from applications.models import Application
from analytics.models import Analytics
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "Seed database with clean, deterministic demo data"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10)
        parser.add_argument("--jobs", type=int, default=30)
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        fake = Faker()

        if options["clear"]:
            self.clear()

        self.stdout.write("Seeding reference data...")
        locations = self.seed_locations()
        categories = self.seed_categories()

        self.stdout.write("Seeding users...")
        job_seekers = self.seed_job_seekers(fake, int(options["users"] * 0.7))
        employers = self.seed_employers(fake, int(options["users"] * 0.25))
        self.seed_admins(fake, options["users"] - len(job_seekers) - len(employers))

        self.stdout.write("Seeding user assets...")
        self.seed_skills(job_seekers)
        self.seed_resumes(fake, job_seekers)

        self.stdout.write("Seeding jobs + applications...")
        jobs = self.seed_jobs(fake, options["jobs"], employers, locations, categories)
        self.seed_applications(fake, job_seekers, jobs)

        self.stdout.write("Seeding notifications + analytics...")
        self.seed_notifications(fake, job_seekers, employers)
        self.seed_analytics(jobs)

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully"))

    # -------------------------
    # CLEAR
    # -------------------------
    def clear(self):
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

        self.stdout.write("Database cleared")

    # -------------------------
    # REFERENCE DATA
    # -------------------------
    def seed_locations(self):
        data = [
            ("Lagos", "Lagos", "Nigeria"),
            ("Abuja", "FCT", "Nigeria"),
            ("Kano", "Kano", "Nigeria"),
            ("Port Harcourt", "Rivers", "Nigeria"),
            ("Ibadan", "Oyo", "Nigeria"),
            ("New York", "New York", "USA"),
            ("London", "England", "UK"),
        ]

        locations = []
        for city, state, country in data:
            loc, _ = Location.objects.get_or_create(
                city=city,
                state=state,
                country=country,
            )
            locations.append(loc)

        return locations

    def seed_categories(self):
        data = [
            ("Software Engineering", "Backend, frontend, fullstack roles"),
            ("Data Science", "ML, AI, analytics roles"),
            ("Design", "UI/UX and product design"),
            ("Product Management", "Product roles"),
            ("DevOps", "Infrastructure and cloud roles"),
            ("Marketing", "Growth and marketing roles"),
        ]

        categories = []
        for name, desc in data:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": desc},
            )
            categories.append(cat)

        return categories

    # -------------------------
    # USERS
    # -------------------------
    def seed_job_seekers(self, fake, count):
        seekers = []
        for _ in range(count):
            user = User.objects.create_user(
                email=fake.unique.email(),
                password="password123",
                role="job_seeker",
            )
            seekers.append(
                JobSeeker.objects.create(
                    user=user,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number()[:15],
                )
            )
        return seekers

    def seed_employers(self, fake, count):
        employers = []
        for _ in range(count):
            user = User.objects.create_user(
                email=fake.unique.email(),
                password="password123",
                role="employer",
            )
            employers.append(
                Employer.objects.create(
                    user=user,
                    company_name=fake.company(),
                    company_description=fake.text(),
                    website=fake.url(),
                )
            )
        return employers

    def seed_admins(self, fake, count):
        for _ in range(count):
            User.objects.create_user(
                email=fake.unique.email(),
                password="admin123",
                role="admin",
            )

    # -------------------------
    # JOB DATA
    # -------------------------
    def seed_jobs(self, fake, count, employers, locations, categories):
        jobs = []

        titles = [
            "Backend Engineer",
            "Frontend Developer",
            "Fullstack Engineer",
            "Data Scientist",
            "DevOps Engineer",
            "Product Manager",
        ]

        for _ in range(count):
            job = Job.objects.create(
                employer=random.choice(employers),
                title=random.choice(titles),
                description=fake.paragraph(nb_sentences=6),
                location=random.choice(locations),
                category=random.choice(categories),
                salary_range=f"${random.randint(60, 150)}k - ${random.randint(150, 250)}k",
                job_type=random.choice(["full-time", "part-time", "remote"]),
                expires_at=timezone.now() + timedelta(days=random.randint(20, 90)),
                is_active=random.choice([True, True, True, False]),
            )
            jobs.append(job)

        return jobs

    # -------------------------
    # APPLICATIONS
    # -------------------------
    def seed_applications(self, fake, seekers, jobs):
        for job in jobs:
            applicants = random.sample(seekers, k=random.randint(2, min(6, len(seekers))))

            for seeker in applicants:
                resume = seeker.resumes.first()
                if not resume:
                    continue

                Application.objects.create(
                    job_seeker=seeker,
                    job=job,
                    resume=resume,
                    cover_letter=fake.paragraph(nb_sentences=4),
                    status=random.choice(["pending", "reviewed", "rejected", "accepted"]),
                )

    # -------------------------
    # SKILLS
    # -------------------------
    def seed_skills(self, seekers):
        skills = ["Python", "Django", "React", "SQL", "AWS", "Docker"]

        for seeker in seekers:
            for skill in random.sample(skills, k=3):
                Skill.objects.create(name=skill, user=seeker.user)

    # -------------------------
    # RESUMES
    # -------------------------
    def seed_resumes(self, fake, seekers):
        for seeker in seekers:
            content = f"{seeker.first_name} {seeker.last_name} Resume"
            file = ContentFile(content.encode())

            resume = Resume(job_seeker=seeker)
            resume.file_path.save(f"resume_{seeker.user.email}.txt", file)

    # -------------------------
    # NOTIFICATIONS
    # -------------------------
    def seed_notifications(self, fake, seekers, employers):
        users = [s.user for s in seekers] + [e.user for e in employers]

        for user in users:
            for _ in range(random.randint(1, 3)):
                Notification.objects.create(
                    user=user,
                    message=fake.sentence(),
                    is_read=random.choice([True, False]),
                )

    # -------------------------
    # ANALYTICS
    # -------------------------
    def seed_analytics(self, jobs):
        for job in jobs:
            Analytics.objects.create(
                job=job,
                date=timezone.now().date(),
                views=random.randint(5, 120),
                applications=random.randint(0, 15),
            )