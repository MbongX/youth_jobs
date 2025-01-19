# Youth Jobs API Documentation

## Authentication

### Register User
```http
POST /register
```

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "user_type": "employer|applicant",
    "company_name": "string (required for employers)"
}
```

**Response:**
```json
{
    "message": "Registration successful",
    "user_id": "integer"
}
```

### Login
```http
POST /login
```

**Request Body:**
```json
{
    "email": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "user_type": "string"
    }
}
```

## Jobs

### List Jobs
```http
GET /jobs
```

**Query Parameters:**
- `page` (integer): Page number
- `per_page` (integer): Items per page
- `location` (string): Filter by location
- `job_type` (string): Filter by job type
- `skills` (string): Filter by required skills

**Response:**
```json
{
    "jobs": [
        {
            "id": "integer",
            "title": "string",
            "company": "string",
            "description": "string",
            "requirements": "string",
            "location": "string",
            "job_type": "string",
            "salary_range": "string",
            "skills_required": "string",
            "posted_date": "datetime"
        }
    ],
    "total": "integer",
    "pages": "integer"
}
```

### Get Job Details
```http
GET /job/<id>
```

**Response:**
```json
{
    "id": "integer",
    "title": "string",
    "company": "string",
    "description": "string",
    "requirements": "string",
    "location": "string",
    "job_type": "string",
    "salary_range": "string",
    "skills_required": "string",
    "posted_date": "datetime",
    "employer": {
        "id": "integer",
        "company_name": "string"
    }
}
```

### Create Job
```http
POST /jobs/create
```

**Request Body:**
```json
{
    "title": "string",
    "description": "string",
    "requirements": "string",
    "location": "string",
    "job_type": "string",
    "salary_range": "string",
    "skills_required": "string"
}
```

### Apply for Job
```http
POST /job/<id>/apply
```

**Request Body:**
```json
{
    "resume_id": "integer",
    "cover_letter": "string"
}
```

## Resume Management

### Create/Update Resume
```http
POST /resume/save
```

**Request Body:**
```json
{
    "title": "string",
    "content": {
        "education": [
            {
                "school": "string",
                "degree": "string",
                "graduation_year": "string"
            }
        ],
        "experience": [
            {
                "company": "string",
                "position": "string",
                "duration": "string",
                "description": "string"
            }
        ],
        "skills": ["string"],
        "projects": [
            {
                "name": "string",
                "description": "string"
            }
        ]
    }
}
```

## Messaging

### Send Message
```http
POST /messages/send
```

**Request Body:**
```json
{
    "recipient_id": "integer",
    "subject": "string",
    "body": "string",
    "job_id": "integer (optional)"
}
```

### List Messages
```http
GET /messages
```

**Query Parameters:**
- `folder` (string): "inbox" or "sent"

**Response:**
```json
{
    "messages": [
        {
            "id": "integer",
            "sender": {
                "id": "integer",
                "username": "string"
            },
            "subject": "string",
            "body": "string",
            "timestamp": "datetime",
            "read": "boolean"
        }
    ]
}
```

## Notifications

### List Notifications
```http
GET /notifications
```

**Response:**
```json
{
    "notifications": [
        {
            "id": "integer",
            "title": "string",
            "message": "string",
            "notification_type": "string",
            "timestamp": "datetime",
            "read": "boolean",
            "related_id": "integer"
        }
    ]
}
```

### Mark Notification as Read
```http
POST /notifications/<id>/read
```

**Response:**
```json
{
    "message": "Notification marked as read",
    "notification_id": "integer"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "string",
    "message": "string"
}
```

### 401 Unauthorized
```json
{
    "error": "Unauthorized",
    "message": "Please log in to access this resource"
}
```

### 403 Forbidden
```json
{
    "error": "Forbidden",
    "message": "You don't have permission to perform this action"
}
```

### 404 Not Found
```json
{
    "error": "Not Found",
    "message": "The requested resource was not found"
}
```

## Rate Limiting

- API requests are limited to 100 requests per minute per IP address
- Job creation is limited to 50 jobs per day per employer
- Message sending is limited to 100 messages per day per user

## Authentication

All endpoints except `/login` and `/register` require authentication using session cookies. The server will return a 401 Unauthorized response if the request is not authenticated.
