# AnyWork Backend Documentation

Welcome to the **AnyWork** backend documentation! This guide provides a comprehensive overview of the backend system built using Django, PostgreSQL, Celery, and RabbitMQ. The application is designed to be highly scalable and supports features like user authentication, job posting, resume management, notifications, and analytics.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
   - [Authentication](#authentication)
   - [Job Seekers](#job-seekers)
   - [Employers](#employers)
   - [Job Management](#job-management)
   - [Resume Management](#resume-management)
   - [Applications](#applications)
   - [Notifications](#notifications)
   - [Skills](#skills)
   - [Analytics](#analytics)
   - [Search](#search)
3. [Asynchronous Notifications](#asynchronous-notifications)
4. [User Stories](#user-stories)
5. [Best Practices](#best-practices)

---

## Introduction

**AnyWork** is a web application designed to connect job seekers with employers. The backend is built using the Django framework, with PostgreSQL as the database. Celery and RabbitMQ are used for asynchronous task processing, such as sending email notifications. The system is designed to be scalable, secure, and easy to maintain.

---

## Features

### Authentication

#### User Registration
**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "email": "testuser@gmail.com",
  "password": "testing321",
  "role": "job_seeker"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "user_id": "8b6c295a-4eaa-47f5-964e-6c2efeb35ed5",
      "email": "testuser@gmail.com",
      "role": "job_seeker",
      "created_at": "2025-03-02T16:11:51.378291Z",
      "updated_at": "2025-03-02T16:11:51.378629Z"
    }
  }
}
```

#### Login via JWT
**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "email": "testuser@gmail.com",
  "password": "testing321"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "user_id": "8b6c295a-4eaa-47f5-964e-6c2efeb35ed5",
      "email": "testuser@gmail.com",
      "role": "job_seeker",
      "created_at": "2025-03-02T16:11:51.378291Z",
      "updated_at": "2025-03-02T16:11:51.378629Z"
    }
  }
}
```

#### Login/Register via OAuth
**Endpoint:** `POST /api/auth/google/`

**Request Body:**
```json
{
  "code": "4/0AQSTgQENJgEcYjxIMw9ceWcDIjQlzuKkcRsbiZKzsS9cssu48V0Y9Rk8W_UMI9Vblou3Vg"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "user_id": "c95b0b81-e7b2-41f4-b09b-0ee416d988f9",
      "email": "jubriltayo@gmail.com",
      "role": "",
      "created_at": "2025-03-01T14:23:28.453365Z",
      "updated_at": "2025-03-01T14:23:28.664644Z"
    }
  }
}
```

---

### Job Seekers

#### Update Job Seeker Profile
**Endpoint:** `PUT /api/jobseekers/{user_id}/`

**Request Body:**
```json
{
  "first_name": "Ben",
  "last_name": "Carson",
  "phone_number": "080444555666"
}
```

**Response:**
```json
{
  "user": "34a64143-12d2-4932-8259-5613e1e27eec",
  "first_name": "Ben",
  "last_name": "Carson",
  "phone_number": "080444555666"
}
```

#### Get Job Seeker Profiles
**Endpoint:** `GET /api/jobseekers/`

**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "user": "34a64143-12d2-4932-8259-5613e1e27eec",
      "first_name": "Ben",
      "last_name": "Carson",
      "phone_number": "080444555666"
    }
  ]
}
```

---

### Employers

#### Update Employer Profile
**Endpoint:** `PUT /api/employers/{user_id}/`

**Request Body:**
```json
{
  "company_name": "Microsoft",
  "company_description": "A tech company",
  "website": "https://www.microsoft.com"
}
```

**Response:**
```json
{
  "user": "b7ff1ac5-a3e6-4707-9ee3-863ff6382abd",
  "company_name": "Microsoft",
  "company_description": "A tech company",
  "website": "https://www.microsoft.com"
}
```

---

### Job Management

#### Create Job Category
**Endpoint:** `POST /api/categories/`

**Request Body:**
```json
{
  "name": "Software Development",
  "description": "Jobs related to software development"
}
```

**Response:**
```json
{
  "category_id": "45cee174-0222-451d-afc3-ef8a7940e027",
  "name": "Software Development",
  "description": "Jobs related to software development"
}
```

#### Create Job Location
**Endpoint:** `POST /api/locations/`

**Request Body:**
```json
{
  "city": "Abeokuta",
  "state": "Ogun",
  "country": "Nigeria"
}
```

**Response:**
```json
{
  "location_id": "e7df170d-9bba-41f6-9645-ae50ec0ed572",
  "city": "Abeokuta",
  "state": "Ogun",
  "country": "Nigeria"
}
```

#### Create Job Posting
**Endpoint:** `POST /api/jobs/`

**Request Body:**
```json
{
  "title": "Software Engineer",
  "description": "We are looking for a skilled software engineer.",
  "location": "e7df170d-9bba-41f6-9645-ae50ec0ed572",
  "category": "45cee174-0222-451d-afc3-ef8a7940e027",
  "salary_range": "$80,000 - $100,000",
  "job_type": "full-time",
  "expires_at": "2025-12-12"
}
```

**Response:**
```json
{
  "job_id": "2f53287a-13b2-4ea1-9c79-a0d6b930581d",
  "title": "Software Engineer",
  "description": "We are looking for a skilled software engineer.",
  "salary_range": "$80,000 - $100,000",
  "job_type": "full-time",
  "posted_at": "2025-03-04T20:51:00.718945Z",
  "expires_at": "2025-12-12T00:00:00Z",
  "is_active": true,
  "employer": "89824eaf-233f-45e1-a417-262e8333c977",
  "location": "e7df170d-9bba-41f6-9645-ae50ec0ed572",
  "category": "45cee174-0222-451d-afc3-ef8a7940e027"
}
```

---

### Resume Management

#### Upload Resume
**Endpoint:** `POST /api/resumes/`

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```
job_seeker="9a6a44cd-d90d-4418-856f-7b192d3bb3c5"
file_path=@"/path/to/resume.pdf"
```

**Response:**
```json
{
  "resume_id": "1d5d5ddd-c18f-4442-b784-81ace316b13e",
  "file_path": "http://127.0.0.1:8000/media/resumes/testresume.pdf",
  "checksum": "9c1a7d15907fb2e3e920404ec081497cc4ab86f233822d721582cf4108fe70f4",
  "uploaded_at": "2025-03-05T22:56:15.360311Z",
  "job_seeker": "9a6a44cd-d90d-4418-856f-7b192d3bb3c5"
}
```

---

### Applications

#### Create Application
**Endpoint:** `POST /api/applications/`

**Request Body:**
```json
{
  "job_seeker": "34a64143-12d2-4932-8259-5613e1e27eec",
  "job": "2f53287a-13b2-4ea1-9c79-a0d6b930581d",
  "resume": "1d5d5ddd-c18f-4442-b784-81ace316b13e",
  "cover_letter": "I am excited to apply for this position."
}
```

**Response:**
```json
{
  "application_id": "7380e23f-d34b-4e5a-aa99-0d4953ed3654",
  "cover_letter": "I am excited to apply for this position.",
  "status": "pending",
  "applied_at": "2025-03-06T06:37:42.030094Z",
  "job_seeker": "34a64143-12d2-4932-8259-5613e1e27eec",
  "job": "2f53287a-13b2-4ea1-9c79-a0d6b930581d",
  "resume": "1d5d5ddd-c18f-4442-b784-81ace316b13e"
}
```

#### Update Application Status
**Endpoint:** `PATCH /api/applications/{application_id}/`

**Request Body:**
```json
{
  "status": "accepted"
}
```

**Response:**
```json
{
  "application_id": "7380e23f-d34b-4e5a-aa99-0d4953ed3654",
  "cover_letter": "I am excited to apply for this position.",
  "status": "accepted",
  "applied_at": "2025-03-06T06:37:42.030094Z",
  "job_seeker": "34a64143-12d2-4932-8259-5613e1e27eec",
  "job": "2f53287a-13b2-4ea1-9c79-a0d6b930581d",
  "resume": "1d5d5ddd-c18f-4442-b784-81ace316b13e"
}
```

---

### Notifications

#### Create Notification
**Endpoint:** `POST /api/notifications/`

**Request Body:**
```json
{
  "user": "89824eaf-233f-45e1-a417-262e8333c977",
  "message": "Your application has been reviewed.",
  "is_read": false
}
```

**Response:**
```json
{
  "notification_id": "7c02c6f8-c9c8-44ce-94e6-75ab62a9a3c5",
  "message": "Your application has been reviewed.",
  "is_read": false,
  "created_at": "2025-03-06T23:30:42.578432Z",
  "user": "89824eaf-233f-45e1-a417-262e8333c977"
}
```

#### Mark Notification as Read
**Endpoint:** `PATCH /api/notifications/{notification_id}/`

**Request Body:**
```json
{
  "is_read": true
}
```

**Response:**
```json
{
  "notification_id": "7c02c6f8-c9c8-44ce-94e6-75ab62a9a3c5",
  "message": "Your application has been reviewed.",
  "is_read": true,
  "created_at": "2025-03-06T23:30:42.578432Z",
  "user": "89824eaf-233f-45e1-a417-262e8333c977"
}
```

---

### Skills

#### Create Skill
**Endpoint:** `POST /api/skills/`

**Request Body:**
```json
{
  "name": "Django"
}
```

**Response:**
```json
{
  "skill_id": "f1ad5a15-4ba0-4a62-bb49-cc8bf1715253",
  "name": "Django",
  "user": "9a6a44cd-d90d-4418-856f-7b192d3bb3c5"
}
```

#### Get Skills
**Endpoint:** `GET /api/skills/`

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "skill_id": "f1ad5a15-4ba0-4a62-bb49-cc8bf1715253",
      "name": "Django",
      "user": "9a6a44cd-d90d-4418-856f-7b192d3bb3c5"
    },
    {
      "skill_id": "75418398-9387-4fff-9228-719dda982d0b",
      "name": "Python",
      "user": "9a6a44cd-d90d-4418-856f-7b192d3bb3c5"
    }
  ]
}
```

---

### Analytics

#### Get Analytics
**Endpoint:** `GET /api/analytics/`

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "analytics_id": "51b52b95-8cbc-46d3-a9be-2d43136d82cd",
      "views": 7,
      "applications": 0,
      "date": "2025-03-08",
      "job": "2f53287a-13b2-4ea1-9c79-a0d6b930581d"
    },
    {
      "analytics_id": "46d1548b-364a-4457-a637-b16f27b57443",
      "views": 6,
      "applications": 2,
      "date": "2025-03-08",
      "job": "c3242a30-1a09-48e1-bb9c-ddba3235a3cd"
    }
  ]
}
```

---

### Search

#### Search Jobs
**Endpoint:** `GET /api/jobs/?search=Software+Engineer`

**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "job_id": "2f53287a-13b2-4ea1-9c79-a0d6b930581d",
      "title": "Software Engineer",
      "description": "We are looking for a skilled software engineer.",
      "salary_range": "$80,000 - $100,000",
      "job_type": "full-time",
      "posted_at": "2025-03-04T20:51:00.718945Z",
      "expires_at": "2025-12-12T00:00:00Z",
      "is_active": true,
      "employer": "89824eaf-233f-45e1-a417-262e8333c977",
      "location": "e7df170d-9bba-41f6-9645-ae50ec0ed572",
      "category": "45cee174-0222-451d-afc3-ef8a7940e027"
    }
  ]
}
```

---

### Asynchronous Notifications

- **Job Seekers** receive email notifications when:
  - They successfully complete an application.
  - A decision is reached by the employer on their application.

---

## User Stories

1. **Job Seeker Registration:**
   - As a job seeker, I want to register on the platform so that I can apply for jobs.
   - **Endpoint:** `POST /api/auth/register/`

2. **Job Application:**
   - As a job seeker, I want to apply for a job by uploading my resume and cover letter.
   - **Endpoint:** `POST /api/applications/`

3. **Employer Job Posting:**
   - As an employer, I want to post a job so that I can attract potential candidates.
   - **Endpoint:** `POST /api/jobs/`

4. **Application Status Update:**
   - As an employer, I want to update the status of a job application so that the job seeker is informed.
   - **Endpoint:** `PATCH /api/applications/{application_id}/`

5. **Notification:**
   - As a job seeker, I want to receive notifications when my application status changes.
   - **Endpoint:** `POST /api/notifications/`

---

## Best Practices

1. **Scalability:**
   - Use Celery and RabbitMQ for asynchronous task processing to handle high loads.
   - Optimize database queries and use indexing for faster data retrieval.

2. **Security:**
   - Use JWT for secure authentication.
   - Validate all incoming data to prevent SQL injection and other attacks.

3. **Maintainability:**
   - Follow Django's best practices for project structure.
   - Write unit tests for all endpoints to ensure reliability.

4. **Documentation:**
   - Keep the API documentation up-to-date.
   - Use tools like Swagger for interactive API documentation.

---

## Developer Information

**Name:** Tayo Jubril  
**Email:** [jubriltayo@gmail.com](mailto:jubriltayo@gmail.com)  
**GitHub:** [https://github.com/jubriltayo](https://github.com/jubriltayo)  
**LinkedIn:** [https://www.linkedin.com/in/jubril-tayo/](https://www.linkedin.com/in/jubril-tayo/)  

---

## Conclusion

Thank you for exploring the **AnyWork** backend documentation! If you have any questions, feedback, or need further assistance, feel free to reach out to the developer via the contact information provided above. Contributions, suggestions, and collaborations are always welcome. Happy coding! 🚀