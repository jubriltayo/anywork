# 💼 AnyWork

> **Production-ready job board REST API with role-based access control, atomic analytics, async email notifications, and SHA-256 resume deduplication**

AnyWork is a full-featured job board backend built with Django and PostgreSQL. It serves two distinct user types (job seekers and employers), each with their own isolated data surface, permissions, and notification pipeline. The API is fully deployed and documented via an interactive Swagger UI.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.3-blue.svg)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/Celery-5.6-brightgreen.svg)](https://docs.celeryq.dev/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-orange.svg)](https://www.rabbitmq.com/)

**Live API:** [anywork.onrender.com](https://anywork.onrender.com/)  
**API Docs:** [anywork.onrender.com](https://anywork.onrender.com/)  
**Frontend:** [AnyWork Frontend Repository](https://github.com/jubriltayo/anywork-frontend)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Technical Highlights](#-technical-highlights)
- [System Architecture](#-system-architecture)
- [API Surface](#-api-surface)
- [Key Implementation Details](#-key-implementation-details)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running the Project](#-running-the-project)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)

---

## 🎯 Overview

AnyWork connects job seekers with employers through a structured REST API with strict role enforcement at every layer. The system handles the full hiring workflow: job postings, resume uploads, applications, status transitions, and email notifications, all with production-grade reliability patterns.

### What This API Does

- ✅ Role-based user registration and authentication (job seeker / employer / admin)
- ✅ JWT authentication with simplejwt (email-only custom user model)
- ✅ Job postings with full-text search, category, location, and type filtering
- ✅ Dual job viewset — public browsing (`/jobs/`) and employer management (`/employer/jobs/`)
- ✅ Resume upload with SHA-256 duplicate detection and physical file cleanup on delete
- ✅ Application tracking with role-restricted status transitions
- ✅ Atomic view and application count tracking using database-level `F()` expressions
- ✅ In-app notifications triggered automatically on application status changes
- ✅ Async email delivery via Celery + RabbitMQ, with graceful synchronous fallback
- ✅ Per-role skill visibility (job seekers see their own; employers see skills of their applicants)
- ✅ Management command to seed the database with realistic demo data
- ✅ Interactive Swagger UI with Bearer auth support

---

## ⚙️ Technical Highlights

### Dual-Surface Permission Architecture

Two separate viewsets serve the same `Job` model with completely different permission and queryset logic:

```python
# Public browsing — anyone reads, only employers write
class JobViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEmployerWriteOnly]

    def get_queryset(self):
        return Job.objects.filter(is_active=True)  # All active jobs, no owner filter


# Employer management — employer-only, scoped to their own jobs
class EmployerJobViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEmployerReadWrite]

    def get_queryset(self):
        return Job.objects.filter(employer=user.employer)  # Only their jobs
```

`IsEmployerReadWrite` enforces object-level ownership, an employer cannot update another employer's posting even with a valid token.

---

### Atomic Analytics Tracking

View and application counts are incremented at the database level to prevent race conditions under concurrent load:

```python
def track_job_view(job):
    with transaction.atomic():
        analytics, created = Analytics.objects.select_for_update().get_or_create(
            job=job,
            date=today,
            defaults={'views': 1}
        )
        if not created:
            Analytics.objects.filter(
                analytics_id=analytics.analytics_id
            ).update(views=F('views') + 1)
```

Using `select_for_update()` + `F()` expressions ensures no two concurrent requests overwrite each other's increment, a correctness issue that naive `obj.views += 1` approaches miss entirely.

---

### SHA-256 Resume Deduplication

Duplicate resume uploads are caught before hitting the database. The checksum is computed in the serializer at validation time:

```python
def validate(self, data):
    sha256 = hashlib.sha256()
    for chunk in file.chunks():
        sha256.update(chunk)
    checksum = sha256.hexdigest()

    if Resume.objects.filter(checksum=checksum, job_seeker=job_seeker).exists():
        raise serializers.ValidationError(
            "You have already uploaded a resume with the same content."
        )
    data['checksum'] = checksum
    return data
```

The model's `delete()` method is also overridden to remove the physical file from storage when a resume record is deleted, preventing orphaned files accumulating on disk.

---

### Graceful Async Degradation

Email tasks are dispatched via Celery in environments where a broker is available. In constrained deployments (e.g. free-tier hosting without a managed broker), a `USE_ASYNC_TASKS` flag routes tasks synchronously through the same interface, no code changes required at the call site:

```python
# utils/async_handler.py
def run_task(task, *args, **kwargs):
    if settings.USE_ASYNC_TASKS:
        return task.delay(*args, **kwargs)
    return task(*args, **kwargs)

# Usage — identical regardless of environment
run_task(send_application_creation_email, user.email)
```

This pattern decouples task dispatch from infrastructure availability, making the service deployable without a broker while preserving full async capability when one is present.

---

### Status-Triggered Notification Pipeline

When an employer updates an application status, two things happen automatically: an in-app notification is created and an async email is dispatched, without any coupling to the view layer:

```python
# applications/models.py
def save(self, *args, **kwargs):
    old_status = Application.objects.get(pk=self.pk).status if self.pk else None
    super().save(*args, **kwargs)

    if old_status and old_status != self.status:
        Notification.objects.create(
            user=self.job_seeker.user,
            message=f"Your application for {self.job.title} has been {self.status}"
        )
        run_task(send_application_status_change_notification, self.application_id)
```

---

## 🏗️ System Architecture

### Application Layer Diagram

```mermaid
graph TD
    Client[Client / Frontend] --> Auth[Auth Layer]

    Auth --> |JWT Token| API[Django REST API]

    API --> Users[Users App<br/>JobSeeker · Employer]
    API --> Jobs[Jobs App<br/>Job · Location · Category]
    API --> Applications[Applications App<br/>Application]
    API --> Resumes[Resumes App<br/>Resume · Checksum]
    API --> Notifications[Notifications App]
    API --> Skills[Skills App]
    API --> Analytics[Analytics App]

    Applications --> |Status Change| NotifPipeline[Notification Pipeline]
    NotifPipeline --> InApp[In-App Notification]
    NotifPipeline --> AsyncHandler[run_task]
    AsyncHandler --> |USE_ASYNC_TASKS=True| Celery[Celery Worker]
    AsyncHandler --> |USE_ASYNC_TASKS=False| SyncEmail[Synchronous Email]
    Celery --> RabbitMQ[RabbitMQ Broker]
    RabbitMQ --> SMTP[SMTP Provider]
    SyncEmail --> SMTP

    Jobs --> |retrieve| AnalyticsTracker[Atomic View Counter]
    Applications --> |create| AppTracker[Atomic Application Counter]
    AnalyticsTracker --> DB[(PostgreSQL)]
    AppTracker --> DB

    Resumes --> |SHA-256| DupeCheck[Duplicate Detection]
    DupeCheck --> DB

    style API fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    style NotifPipeline fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style AsyncHandler fill:#fff3cd,stroke:#ffc107,stroke-width:2px
    style DB fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
```

### Role-Based Data Isolation

```mermaid
graph LR
    subgraph "Job Seeker"
        JS_Jobs[Browse all active jobs]
        JS_Apply[Submit applications]
        JS_Resume[Upload resumes]
        JS_Skills[Manage own skills]
        JS_Notif[View own notifications]
        JS_Analytics[View analytics for applied jobs]
    end

    subgraph "Employer"
        EM_PostJob[Post and manage own jobs]
        EM_ViewApps[View applications to own jobs]
        EM_UpdateStatus[Update application status]
        EM_ViewSkills[View applicant skills]
        EM_Analytics[View analytics for own job postings]
    end

    subgraph "Data Boundary"
        DB_Jobs[(Jobs)]
        DB_Apps[(Applications)]
        DB_Resumes[(Resumes)]
    end

    JS_Jobs --> DB_Jobs
    JS_Apply --> DB_Apps
    EM_PostJob --> DB_Jobs
    EM_ViewApps --> DB_Apps
    JS_Resume --> DB_Resumes
```

### Request Flow: Application Status Change

```mermaid
sequenceDiagram
    participant Employer
    participant API as Django API
    participant DB as PostgreSQL
    participant Handler as run_task()
    participant Celery
    participant SMTP

    Employer->>API: PATCH /api/applications/{id}/ {status: "accepted"}
    API->>API: Check IsJobSeekerOrEmployer permission
    API->>API: Check employer owns the job (object permission)
    API->>API: Block if request.user is job_seeker (status lock)
    API->>DB: Save updated application
    DB->>DB: Model.save() detects status change
    DB->>DB: Create Notification record
    DB->>Handler: run_task(send_email, application_id)

    alt USE_ASYNC_TASKS=True
        Handler->>Celery: task.delay(application_id)
        Celery->>DB: Fetch application + job seeker email
        Celery->>SMTP: Send status update email
    else USE_ASYNC_TASKS=False
        Handler->>DB: Fetch application + job seeker email
        Handler->>SMTP: Send status update email (synchronous)
    end

    API-->>Employer: 200 OK — updated application data
```

---

## 📖 API Surface

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register a new user (job_seeker or employer) |
| `POST` | `/api/auth/login/` | Obtain JWT access + refresh tokens |
| `POST` | `/api/auth/logout/` | Invalidate refresh token |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |

### Users

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/api/jobseekers/` | List job seeker profiles | Authenticated |
| `PUT/PATCH` | `/api/jobseekers/{user_id}/` | Update own profile | Job seeker only |
| `GET` | `/api/employers/` | List employer profiles | Authenticated |
| `PUT/PATCH` | `/api/employers/{user_id}/` | Update own profile | Employer only |

### Jobs

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/api/jobs/` | Browse all active jobs (supports search + filter) | Public |
| `GET` | `/api/jobs/{job_id}/` | View job details (increments view counter) | Public |
| `POST` | `/api/jobs/` | Create a job posting | Employer only |
| `GET` | `/api/employer/jobs/` | List own job postings | Employer only |
| `PUT/PATCH/DELETE` | `/api/employer/jobs/{job_id}/` | Manage own job posting | Employer (owner only) |
| `GET` | `/api/categories/` | List job categories | Authenticated |
| `GET` | `/api/locations/` | List locations | Authenticated |

**Search & Filter:** `GET /api/jobs/?search=engineer&job_type=remote&location__city=Lagos`

### Applications

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/api/applications/` | Submit an application | Job seeker only |
| `GET` | `/api/applications/` | List own applications | Role-scoped |
| `PATCH` | `/api/applications/{id}/` | Update application status | Employer only |

### Resumes, Skills, Notifications, Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/resumes/` | Upload a resume (PDF, max 10MB, deduped by SHA-256) |
| `GET` | `/api/resumes/` | List own resumes |
| `DELETE` | `/api/resumes/{id}/` | Delete resume (removes physical file) |
| `GET` | `/api/skills/` | View skills (own for job seekers; applicants' for employers) |
| `POST` | `/api/skills/` | Add a skill (job seekers only) |
| `GET` | `/api/notifications/` | List own notifications |
| `PATCH` | `/api/notifications/{id}/mark-as-read/` | Mark notification as read |
| `GET` | `/api/analytics/` | View analytics (role-scoped to own jobs or applied jobs) |

---

## 🛠️ Key Implementation Details

### Custom User Model

Username field is removed entirely. Email is the sole identifier, enforced at the manager level:

```python
class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
```

Registration atomically creates both the `User` and their role-specific profile (`JobSeeker` or `Employer`) in a single call via `create_user()` in `users/auth.py`.

### Job Search and Filtering

Full-text search across title, description, city, and category name. Filter by job type, date range, and location, all handled by `django-filters` and DRF's `SearchFilter`:

```python
search_fields = ['title', 'description', 'location__city', 'category__name']
filterset_class = JobFilter  # title, location__city, job_type, posted_at range
```

### Application Duplicate Prevention

A database-level `UniqueConstraint` on `(job_seeker, job)` combined with a view-level check prevents double applications:

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['job_seeker', 'job'],
            name='unique_application_per_job'
        )
    ]
```

### Analytics Constraint

One analytics record per job per day, enforced at the database level:

```python
constraints = [
    models.UniqueConstraint(fields=['job', 'date'], name='unique_job_date')
]
```

---

## 📁 Project Structure

```
anywork_backend/
├── core/
│   ├── settings.py          # Environment config, Celery, JWT, logging
│   ├── celery.py            # Celery app with Django settings integration
│   └── urls.py              # Root URLs, Swagger config
│
├── users/
│   ├── models.py            # User (email-only), JobSeeker, Employer
│   ├── manager.py           # Custom UserManager with email validation
│   ├── auth.py              # create_user(), token generation
│   ├── serializers.py       # User, JobSeeker, Employer serializers
│   └── views.py             # Auth views, profile management
│
├── jobs/
│   ├── models.py            # Job, Location, Category
│   ├── views.py             # JobViewSet (public), EmployerJobViewSet (scoped)
│   ├── permissions.py       # IsEmployerWriteOnly, IsEmployerReadWrite
│   └── filters.py           # JobFilter (title, city, type, date range)
│
├── applications/
│   ├── models.py            # Application with status-triggered notification on save()
│   ├── tasks.py             # Celery tasks — creation email, status change email
│   ├── permissions.py       # IsJobSeekerOrEmployer
│   └── views.py             # Role-scoped queryset, employer-only status update
│
├── resumes/
│   ├── models.py            # Resume with SHA-256 checksum, file deletion on delete()
│   ├── serializers.py       # Checksum validation, duplicate detection
│   └── validators.py        # PDF-only, max 10MB
│
├── analytics/
│   ├── models.py            # Analytics (job + date unique constraint)
│   └── utils.py             # track_job_view(), track_job_application() — atomic F()
│
├── notifications/
│   └── views.py             # ReadOnly, user-scoped, mark-as-read action
│
├── skills/
│   └── views.py             # Job seeker sees own; employer sees applicants' skills
│
├── utils/
│   └── async_handler.py     # run_task() — Celery or sync based on USE_ASYNC_TASKS
│
└── users/management/
    └── commands/
        └── seed_data.py     # Full database seeder for demo and testing
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 18.3+
- RabbitMQ 3.12+ *(optional — set `USE_ASYNC_TASKS=False` to skip)*
- [uv](https://docs.astral.sh/uv/) *(package manager)*

### 1. Clone the Repository

```bash
git clone https://github.com/jubriltayo/anywork.git
cd anywork
```

### 2. Install Dependencies

uv handles the virtual environment and dependencies automatically:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash

# Django
SECRET_KEY=your-django-secret-key
DEBUG=True

# Database
DB_NAME=anywork
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Celery (optional — set USE_ASYNC_TASKS=False to run synchronously)
USE_ASYNC_TASKS=False
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672/

# Email (Mailtrap for development)
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your-mailtrap-user
EMAIL_HOST_PASSWORD=your-mailtrap-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@anywork.com
```

### 4. Run Migrations

```bash
uv run manage.py migrate
```

### 5. Seed Demo Data *(optional)*

```bash
uv run manage.py seed_data
```

This creates job seekers, employers, job postings, applications, skills, and analytics records, all with realistic data. Seeded credentials are printed to stdout.


---

## ▶️ Running the Project

### Without Celery (synchronous mode)

```bash
# Set USE_ASYNC_TASKS=False in .env, then:
python manage.py runserver
```

### With Celery (full async)

```bash
# Terminal 1 — Django server
python manage.py runserver

# Terminal 2 — Celery worker
celery -A core worker --loglevel=info
```

### Access the API

- **Swagger UI:** `http://localhost:8000/`
- **ReDoc:** `http://localhost:8000/redoc/`
- **Admin:** `http://localhost:8000/admin/`

---

## 🧪 Demo

### Async Email Notifications

![Celery worker processing both email tasks](demo/celery_logs.png)

*Celery worker receiving and completing both notification tasks (application confirmation
and status change), dispatched via RabbitMQ.*

### Email Delivery

![Mailtrap inbox showing delivered notification emails](demo/mailtrap_email.png)

*Notification emails delivered to the development inbox via Mailtrap.*

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12 |
| **Framework** | Django 6.0 + Django REST Framework |
| **Database** | PostgreSQL 18.3 |
| **Auth** | simplejwt (JWT — email/password) |
| **Async Tasks** | Celery 5.6 + RabbitMQ 3.12 |
| **Search/Filter** | django-filters + DRF SearchFilter |
| **API Docs** | drf-yasg (Swagger + ReDoc) |
| **File Storage** | Django FileField (local / S3-compatible) |
| **Static Files** | WhiteNoise |

---

## 👤 Author

**Tayo Jubril**  
Backend Engineer

- **Email:** jubriltayo@gmail.com
- **GitHub:** [@jubriltayo](https://github.com/jubriltayo)
- **LinkedIn:** [jubril-tayo](https://www.linkedin.com/in/jubril-tayo/)