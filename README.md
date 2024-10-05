# Job Portal
A Django-based Job Listing and Application platform with role-based access for Admins, Employers, and Candidates.

### Project Setup Instructions
Prerequisites
Python 3.7+
Django 3.x or later
Django REST Framework
Django Filters
Django REST Framework SimpleJWT (for token-based authentication)

#### Create and activate a virtual environment
Install required packages (Use requirements.txt)

## API Documentation : 
This project uses JWT (JSON Web Token) for authentication via the SimpleJWT package.
+ Register:
    - URL: /api/auth/register/
    - Method: POST
    - Body:
      {
      "email": "user@example.com",
      "username": "user_name",
      "password": "user_password",
      "role": "Employer" | "Candidate"
      }
    - {
     "id": 1,
     "email": "example@example.com",
     "username": "example_user",
     "role": "Employer"
     }


+ Log in:
    - URL: /api/auth/login/
    - Method: POST
    - {
      "email": "user@example.com",
      "password": "user_password"
      }
    - {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
      }

+ User Role:
    - Endpoint: /api/auth/role/
    - Method: GET
    - Headers: Authorization: Bearer <access_token>
    - {
      "role": "Employer"
      }

+ Create Job Listing :
    - Endpoint: /api/jobs/job-list/
    - Method: POST
    - Headers: Authorization: Bearer <access_token>
    - {
      "title": "Software Developer",
      "description": "Job description here...",
      "location": "City, Country",
      "company": "<company_id>"
      }
    - {
      "id": 1,
      "title": "Software Developer",
      "description": "Job description here...",
      "location": "City, Country",
      "company": "<company_id>"
      }
+ View Job Listings :
    - Endpoint: /api/jobs/job-list/
    - Method: GET
    - Headers: Authorization: Bearer <access_token>
    - [
        {
          "id": 1,
          "title": "Software Developer",
          "description": "Job description here...",
          "location": "City, Country",
          "company": "Company Name"
        }
      ]
+ Apply for Job(Applications creation) :
    - Endpoint: /api/jobs/job-applications/
    - Method: POST
    - Headers: Authorization: Bearer <access_token>
    - {
      "job": "<job_id>",
      "resume":resume.pdf
      "cover_letter": "I am interested in this position..."
      }
    - {
      "id": 1,
      "job": "<job_id>",
      "candidate": "<candidate_id>",
      "cover_letter": "I am interested in this position..."
      }
      
+  View Applications (Employers / Candidates) :
    - Endpoint: /api/jobs/job-applications/
    - Method: GET
    - Headers: Authorization: Bearer <access_token>
    - {
      "id": 1,
      "job": "<job_id>",
      "candidate": "<candidate_id>",
      "cover_letter": "I am interested in this position..."
      }

+ Update Job Application (Employers/Admins) :
    - Endpoint: /api/jobs/job-applications/
    - Method: PATCH
    - Headers: Authorization: Bearer <access_token>
    - {
      "cover_letter": "I am interested in this position..."
      }
    - {
      "cover_letter": "Updated cover letter..."
      }

## Additonal Features

### Company Profiles:
* Employers can create detailed profiles for their companies, including the company’s name, description, location, and website.
* These profiles are visible to candidates when they view job listings, allowing them to learn more about the company before applying.
  
### Email Notifications:
* Email alerts are automatically triggered during certain events:
* When a Candidate submits a job application, they receive a confirmation email.
* These notifications ensure that users are always informed of important updates without needing to constantly check the platform.

### Pagination:
* Job Listings and Applications are paginated to handle large sets of data.
* The API returns a fixed number of records per page (configurable) and provides the necessary links to navigate between pages.

### Filtering:
* Users can filter job listings based on specific fields, such as:
* Location: Filter jobs by city, state, or country.
* Salary: Filter jobs based on the salary range.
* Job Status: Filter jobs based on whether they are active, closed, or pending.
* This functionality allows users to easily narrow down the results to find relevant jobs or applications.

### Search:
* The platform allows users to search job listings by keywords such as job title, company name, or location.
* This search feature provides a simple and intuitive way for candidates to find jobs that match their interests or skills.


## Additional Notes
#### This platform uses JWT (JSON Web Token) authentication to secure API endpoints and manage user sessions. Each user role (Admin, Employer, Candidate) has specific permissions, ensuring role-based access to resources.

### Admin:
* Has full access to all job listings, job applications, and users.
* Can view, update, and delete any job listing or application.
* Admins are prohibited from creating job listings or applying for jobs but can manage all other resources. 

### Employer:
* Can create, update, and delete their own job listings.
* Can view job applications submitted for their job postings.
* Employers can manage their company profile, job listings, and view applications submitted for their job posts.

### Candidate:
* Can view job listings and apply for jobs.
* Can manage their own applications (view, but not update or delete once submitted).
* Candidates are prohibited from creating job listings but can apply for jobs and track the status of their applications.

Each role ensures that users are provided only the necessary level of access to data based on their responsibilities.

  
  
  

      

  





