# AnyWork

This is a backend side of a web app built using the django framework.
It uses a postgresql database

## Features
### Authentication
#### User creation
POST
http://127.0.0.1:8000/api/auth/register/
body
{
  "email": "testuser@gmail.com",
  "password": "testing321",
  "role": "job_seeker"
}

Response
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

#### Login via JWT
POST
http://127.0.0.1:8000/api/auth/login/
body
{
  "email": "testuser@gmail.com",
  "password": "testing321"
}
Response
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMDE4NDAxLCJpYXQiOjE3NDA5MzIwMDEsImp0aSI6ImQxY2VmMWRkOGQyYTQ5NjI5MDc4YmJjMzc2YmNkZjMxIiwidXNlcl9pZCI6IjhiNmMyOTVhLTRlYWEtNDdmNS05NjRlLTZjMmVmZWIzNWVkNSJ9.RhSO5r6Ff-ZeEyaPP9DW309GViUgFVRfmX8515zx_lU",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTM2NDAwMSwiaWF0IjoxNzQwOTMyMDAxLCJqdGkiOiI3Mzk4MmUxZDA3Mjc0MDdmYWVlNGM5Y2IzZmUxNGQxZSIsInVzZXJfaWQiOiI4YjZjMjk1YS00ZWFhLTQ3ZjUtOTY0ZS02YzJlZmViMzVlZDUifQ.NHxb--r2Xcz0h7rbPO4gz_XABxfEDpFxxbQnHJ3x2NU",
    "user": {
      "user_id": "8b6c295a-4eaa-47f5-964e-6c2efeb35ed5",
      "email": "testuser@gmail.com",
      "role": "job_seeker",
      "created_at": "2025-03-02T16:11:51.378291Z",
      "updated_at": "2025-03-02T16:11:51.378629Z"
    }
  }
}

#### Login/Register via OAuth
POST
http://127.0.0.1:8000/api/auth/google/
body
{
  "code": "4/0AQSTgQENJgEcYjxIMw9ceWcDIjQlzuKkcRsbiZKzsS9cssu48V0Y9Rk8W_UMI9Vblou3Vg"
}
Response
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMDE1MjczLCJpYXQiOjE3NDA5Mjg4NzMsImp0aSI6ImZhZjhkZWIyOGY2YTQ5MTVhMWFlZmI3MjhhMzRkNDMyIiwidXNlcl9pZCI6ImM5NWIwYjgxLWU3YjItNDFmNC1iMDliLTBlZTQxNmQ5ODhmOSJ9.isIe4qOtypHDU8paBKUjY5ok3YRVNJfee56F0mdp2KA",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTM2MDg3MywiaWF0IjoxNzQwOTI4ODczLCJqdGkiOiIyNmMzMTY2MGVhZTQ0NmQ1OTUxZWJkYjllYzBiY2YxZCIsInVzZXJfaWQiOiJjOTViMGI4MS1lN2IyLTQxZjQtYjA5Yi0wZWU0MTZkOTg4ZjkifQ.wNMG5EM94y25ImPAENu1g-CJlK5eXtz7qqOPQe3ci-M",
    "user": {
      "user_id": "c95b0b81-e7b2-41f4-b09b-0ee416d988f9",
      "email": "jubriltayo@gmail.com",
      "role": "",
      "created_at": "2025-03-01T14:23:28.453365Z",
      "updated_at": "2025-03-01T14:23:28.664644Z"
    }
  }
}

### JobSeekers
POST/Create -- Disabled because jobseekers profiles are created during user registration

PUT
http://127.0.0.1:8000/api/jobseekers/34a64143-12d2-4932-8259-5613e1e27eec/
Body
{
  "first_name": "Ben",
  "last_name": "Carson",
  "phone_number": "080444555666"
}
Response
{
  "user": "34a64143-12d2-4932-8259-5613e1e27eec",
  "first_name": "Ben",
  "last_name": "Carson",
  "phone_number": "080444555666"
}

GET
http://127.0.0.1:8000/api/jobseekers/
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

### Employers
POST/Create -- Disabled because employee profiles are created during user registration
PUT
http://127.0.0.1:8000/api/employers/b7ff1ac5-a3e6-4707-9ee3-863ff6382abd/
Body
{
  "company_name": "Microsoft",
  "company_description": "A tech company",
  "website": "https://www.microsoft.com"
}
Response
{
  "user": "b7ff1ac5-a3e6-4707-9ee3-863ff6382abd",
  "company_name": "Microsoft",
  "company_description": "A tech company",
  "website": "https://www.microsoft.com"
}




