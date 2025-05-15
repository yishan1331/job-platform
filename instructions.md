## Project Overview

This project is a **Job Platform** web application. The goal is to showcase full-stack development capabilities by building a minimal, functional system that allows users to manage job postings with features such as creation, listing, searching, and filtering.

The application consists of two main components:

1. **Backend (API)** – A RESTful API built with Django and Django Ninja to manage job data, including endpoints for CRUD operations, search, filtering, and user authentication.
2. **Frontend (SPA)** – A single-page application (preferably built with Vue 3 or Nuxt 3) that interacts with the API to present job listings, job details, and allow job creation, with support for multilingual interfaces (English and Traditional Chinese).

### Key Flow

-   **User Login**
    The application uses `django-ninja-jwt` for authentication. Users can log in using valid credentials to obtain a JWT token. Authenticated access is required for creating, updating, and deleting job postings.

-   **Job Posting Creation**
    Authenticated users can create a new job posting by submitting a form that includes required fields such as title, description, location, company name, and expiration date.

-   **Job Listing & Search**
    Users can browse a list of available job postings with support for:

    -   Text search by title, description, and company name
    -   Filtering by job status (active, expired, scheduled)
    -   Sorting by posting or expiration date
    -   Pagination

-   **Job Detail View**
    Users can view the full detail of a specific job by navigating to its detail page.

-   **Job Update & Delete**
    Authenticated users can update or delete an existing job posting. Company name is immutable after creation.

-   **Language Switching**
    Users can toggle between English and Traditional Chinese interface using a language switcher.

-   **URL-State Synchronization**
    The search, filter, and pagination parameters are preserved in the URL to support navigation, refreshing, and deep linking.

This document provides instructions and context for understanding and extending the current codebase.

## Core Functionalities

The system is composed of two primary modules: **Backend API** and **Frontend SPA**. Each module handles specific responsibilities and together form a fully functional job management platform.

---

### Backend API (Django + Django Ninja)

-   **Authentication**

    -   JWT-based login using `django-ninja-jwt`
    -   Token-based access to protected endpoints (job creation, update, deletion)
    -   Secured endpoints require `Authorization: Bearer <token>`

-   **Job Posting Management**

    -   Create a new job
    -   Retrieve a list of jobs (with filters, search, pagination, and sorting)
    -   Retrieve a single job by ID
    -   Update an existing job (except company name)
    -   Delete a job

-   **Search and Filtering**

    -   Search by `title`, `description`, and `company_name`
    -   Filter by:
        -   `status`: active, expired, scheduled
        -   Any other field (e.g. `location`, `skills`)
    -   Sort by `posting_date` or `expiration_date`
    -   Paginated responses

-   **Input Validation & Documentation**

    -   Use Django Ninja's `Schema` for input validation
    -   Auto-generate OpenAPI docs with type-safe responses

-   **Testing**
    -   Use `pytest` and `pytest-django`
    -   Perform API-level tests by calling HTTP endpoints directly

#### Endpoints

    | Method | Endpoint      | Description                                     |
    | ------ | ------------- | ----------------------------------------------- |
    | POST   | `/auth/login` | Obtain JWT token via `django-ninja-jwt`         |
    | POST   | `/jobs`       | Create a new job posting                        |
    | GET    | `/jobs`       | Retrieve job list (with search/filter)          |
    | GET    | `/jobs/{id}`  | Get a single job posting by ID                  |
    | PUT    | `/jobs/{id}`  | Update an existing job (company name immutable) |
    | DELETE | `/jobs/{id}`  | Delete a job posting                            |

#### Supported Parameters for `GET /jobs`

-   `search`: keyword for title, description, company_name
-   `status`: `active` | `expired` | `scheduled`
-   `ordering`: `posting_date` | `expiration_date`
-   Other filters: `location`, `required_skills`, `salary_range`, etc.
-   Pagination: `page`, `page_size`

#### Job Model Fields

-   `title`: string
-   `description`: string
-   `location`: string
-   `salary_range`: string or object
-   `company_name`: string (immutable once created)
-   `posting_date`: date
-   `expiration_date`: date
-   `required_skills`: list of strings

---

### Frontend SPA (Vue 3 Preferred)

-   **Authentication**

    -   Login form that obtains JWT and stores token securely (e.g. in memory or localStorage)
    -   Use token in Authorization header for protected API calls

-   **Job List Page**

    -   Display paginated list of jobs
    -   Search, filter, and sort functionality
    -   Query parameters synced with URL
    -   Supports browser navigation (back/forward)

-   **Job Detail Page**

    -   Displays full job information
    -   Routed via job ID

-   **Job Creation Form**

    -   Authenticated users can submit a new job post
    -   Validate required fields
    -   Submit data to `/jobs` endpoint

-   **Job Editing and Deletion**

    -   Allow updating job fields (except company name)
    -   Delete job functionality

-   **Internationalization (i18n)**

    -   Toggle between Traditional Chinese and English
    -   Dynamic language switching across UI

-   **Responsive UI**

    -   Mobile-friendly layout
    -   Clean and accessible design

-   **Custom Component or Advanced UI**
    -   At least one custom or animated component showcasing design skills
    -   Could include graphics, icons, transitions, or media responsiveness

---

These core functionalities lay the foundation for both feature completeness and code evaluation based on quality, maintainability, and architectural decisions.

## Documentation

(to fill in later)

## Current Project Structure

(to fill in later)
