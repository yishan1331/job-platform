# 📐 Schema Design

## 🧑‍💼 User

| Field      | Type         | Required | Default           | Description                |
| ---------- | ------------ | -------- | ----------------- | -------------------------- |
| id         | UUID / int   | ✅       |                   | Primary key                |
| email      | varchar(100) | ✅       |                   | Unique user email          |
| password   | varchar(50)  | ✅       |                   | Hashed password            |
| role       | varchar(20)  | ✅       |                   | 'recruiter' or 'applicant' |
| full_name  | varchar(50)  | 🟡       |                   | Display name               |
| is_active  | boolean      | 🟡       | true              | Active/inactive status     |
| last_login | timestamp    | 🟡       |                   | Last login timestamp       |
| created_at | timestamp    | ✅       | current timestamp | User registration time     |
| updated_at | timestamp    | ✅       | current timestamp | when update auto_now       |
| deleted_at | timestamp    | 🟡       |                   |                            |

---

## 🏢 Company

| Field       | Type              | Required | Default           | Description                  |
| ----------- | ----------------- | -------- | ----------------- | ---------------------------- |
| id          | UUID / int        | ✅       |                   | Primary key                  |
| name        | varchar(100)      | ✅       |                   | Unique company name          |
| location    | varchar(512)      | ✅       |                   | Company address/location     |
| description | longtext          | 🟡       |                   | Optional company description |
| website     | varchar(256)      | 🟡       |                   | Company official site        |
| logo_url    | varchar(512)      | 🟡       |                   | Logo or brand image URL      |
| owner       | ForeignKey → User | ✅       |                   | Must be a recruiter          |
| is_active   | boolean           | 🟡       | true              | Active/inactive status       |
| created_by  | ForeignKey → User | ✅       |                   |                              |
| modified_by | ForeignKey → User | ✅       |                   |                              |
| created_at  | timestamp         | ✅       | current timestamp | Time the company was created |
| updated_at  | timestamp         | ✅       | current timestamp | when update auto_now         |
| deleted_at  | timestamp         | 🟡       |                   |                              |

---

## 📄 JobPosting

| Field           | Type                 | Required | Default           | Description                                   |
| --------------- | -------------------- | -------- | ----------------- | --------------------------------------------- |
| id              | UUID / int           | ✅       |                   | Primary key                                   |
| title           | varchar(64)          | ✅       |                   | Job title                                     |
| description     | longtext             | ✅       |                   | Job description                               |
| location        | varchar(512)         | ✅       |                   | Job location                                  |
| salary_range    | JSON                 | ✅       |                   | Pay range; flexible format                    |
| salary_type     | enum                 | ✅       |                   | `annual`, `monthly`, or `hourly`              |
| required_skills | JSON                 | ✅       |                   | List of required skills (as array of strings) |
| posting_date    | dateTime             | ✅       |                   | Date when job becomes visible                 |
| expiration_date | dateTime             | 🟡       |                   | Date when job becomes inactive                |
| apply_url       | varchar(512)         | 🟡       |                   | External application link (if applicable)     |
| type            | enum                 | 🟡       |                   | Job type: full-time / part-time / internship  |
| company         | ForeignKey → Company | ✅       |                   | Associated company                            |
| created_by      | ForeignKey → User    | ✅       |                   | Must be a recruiter, and owner of the company |
| modified_by     | ForeignKey → User    | ✅       |                   | Must be a recruiter, and owner of the company |
| is_active       | boolean              | 🟡       | true              | Soft-delete or publish status                 |
| created_at      | timestamp            | ✅       | current timestamp | When the job was created                      |
| updated_at      | timestamp            | 🟡       | current timestamp | when update auto_now                          |
| deleted_at      | timestamp            | 🟡       |                   |                                               |

---

## 📌 Relationships Summary

-   `User` 1️⃣ → 🔁 `Company`: One-to-many (a recruiter may own multiple companies)
-   `User` 1️⃣ → 🔁 `JobPosting`: One-to-many (job posts created by recruiter)
-   `Company` 1️⃣ → 🔁 `JobPosting`: One-to-many (a company can have many jobs)

---
