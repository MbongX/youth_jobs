# Database Schema Documentation

## Overview

The Youth Jobs platform uses SQLite with SQLAlchemy ORM. The database schema is designed to support job postings, applications, messaging, and notifications between employers and job seekers.

## Tables

### User
Stores both employer and applicant information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| username | String(80) | Unique, Not Null | User's display name |
| email | String(120) | Unique, Not Null | User's email address |
| password | String(200) | Not Null | Hashed password |
| user_type | String(20) | Not Null | 'employer' or 'applicant' |
| company_name | String(100) | Nullable | Company name (for employers) |

**Relationships:**
- One-to-Many with Job (as employer)
- One-to-Many with Resume (as applicant)
- One-to-Many with JobApplication (as applicant)
- One-to-Many with Message (as sender and recipient)
- One-to-Many with Notification

### Job
Stores job posting information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| employer_id | Integer | Foreign Key (user.id) | Reference to employer |
| title | String(100) | Not Null | Job title |
| description | Text | Not Null | Job description |
| requirements | Text | Not Null | Job requirements |
| location | String(100) | Not Null | Job location |
| job_type | String(50) | Not Null | Full-time, Part-time, etc. |
| salary_range | String(50) | Nullable | Expected salary range |
| skills_required | Text | Not Null | Required skills |
| posted_date | DateTime | Not Null | Posting timestamp |
| is_active | Boolean | Not Null | Job availability status |

**Relationships:**
- Many-to-One with User (employer)
- One-to-Many with JobApplication

### Resume
Stores applicant resumes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| user_id | Integer | Foreign Key (user.id) | Reference to applicant |
| title | String(100) | Not Null | Resume title |
| content | JSON | Not Null | Resume content |
| created_at | DateTime | Not Null | Creation timestamp |
| updated_at | DateTime | Not Null | Last update timestamp |

**Relationships:**
- Many-to-One with User (applicant)
- One-to-Many with JobApplication

### JobApplication
Tracks job applications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| job_id | Integer | Foreign Key (job.id) | Reference to job |
| applicant_id | Integer | Foreign Key (user.id) | Reference to applicant |
| resume_id | Integer | Foreign Key (resume.id) | Reference to resume |
| cover_letter | Text | Not Null | Application cover letter |
| status | String(20) | Not Null | Application status |
| applied_date | DateTime | Not Null | Application timestamp |

**Relationships:**
- Many-to-One with Job
- Many-to-One with User (applicant)
- Many-to-One with Resume

### Message
Handles internal messaging.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| sender_id | Integer | Foreign Key (user.id) | Reference to sender |
| recipient_id | Integer | Foreign Key (user.id) | Reference to recipient |
| subject | String(100) | Not Null | Message subject |
| body | Text | Not Null | Message content |
| timestamp | DateTime | Not Null | Sent timestamp |
| read | Boolean | Not Null | Read status |
| job_id | Integer | Foreign Key (job.id) | Related job (optional) |

**Relationships:**
- Many-to-One with User (sender)
- Many-to-One with User (recipient)
- Many-to-One with Job (optional)

### Notification
Manages system notifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| user_id | Integer | Foreign Key (user.id) | Reference to user |
| title | String(200) | Not Null | Notification title |
| message | Text | Not Null | Notification content |
| timestamp | DateTime | Not Null | Creation timestamp |
| read | Boolean | Not Null | Read status |
| notification_type | String(50) | Not Null | Type of notification |
| related_id | Integer | Nullable | Related entity ID |

**Relationships:**
- Many-to-One with User

### JobPreference
Stores applicant job preferences.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique identifier |
| user_id | Integer | Foreign Key (user.id) | Reference to applicant |
| job_type | String(50) | Not Null | Preferred job type |
| location | String(100) | Not Null | Preferred location |
| salary_expectation | String(50) | Nullable | Expected salary range |
| skills | Text | Not Null | Skills possessed |

**Relationships:**
- Many-to-One with User

## Indexes

1. User Table:
   - email_idx (email)
   - username_idx (username)

2. Job Table:
   - employer_idx (employer_id)
   - location_idx (location)
   - posted_date_idx (posted_date)

3. JobApplication Table:
   - applicant_idx (applicant_id)
   - job_idx (job_id)
   - status_idx (status)

4. Message Table:
   - sender_idx (sender_id)
   - recipient_idx (recipient_id)
   - timestamp_idx (timestamp)

5. Notification Table:
   - user_notification_idx (user_id, timestamp)
   - read_status_idx (read)

## Constraints

1. User:
   - Unique email addresses
   - Unique usernames
   - Valid user_type values

2. Job:
   - Valid job_type values
   - posted_date cannot be in the future

3. JobApplication:
   - Valid status values
   - One application per job per applicant

4. Message:
   - sender_id cannot equal recipient_id
   - timestamp cannot be in the future

5. Notification:
   - Valid notification_type values
   - timestamp cannot be in the future

## Data Types

- String fields use VARCHAR with appropriate length limits
- Text fields use TEXT type for unlimited length
- Dates use DATETIME type
- Boolean fields use BOOLEAN type
- IDs use INTEGER type
- JSON content uses JSON type (for Resume content)

## Cascading Behavior

1. User deletion:
   - Cascades to: Resumes, JobApplications, Messages, Notifications
   - Jobs are deactivated but not deleted

2. Job deletion:
   - Cascades to: JobApplications
   - Related messages and notifications are preserved

3. Resume deletion:
   - Cascades to: JobApplications using that resume

## Migrations

Database migrations are handled using Flask-Migrate (Alembic). Migration files are stored in the `migrations` directory.
