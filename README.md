# Introduction

This project is a CRUD (Create, Read, Update, Delete) API built with FastAPI and MongoDB. The API allows users to manage job postings, including the ability to create, retrieve, update, and delete job records. The API also includes user authentication for secure access to the job posting operations.

# Features

- **User Authentication**: Users can register and login to access the job posting operations.
- **CRUD Operations**: Users can create, retrieve, update, and delete job records.
- **MongoDB Database**: The API uses MongoDB to store job records and user information.
- **Validation**: The API validates user input to ensure data integrity.

# File Structure

The project has the following file structure:

```
.
├── auth.py
├── database.py
├── .env
├── main.py
├── models.py
└── README.md
```

- `auth.py`: Contains the user authentication logic.
- `database.py`: Contains the MongoDB database connection logic.
- `.env`: Contains environment variables for the project.
- `main.py`: Contains the FastAPI application and API endpoints.
- `models.py`: Contains the Pydantic models for the API.

# Installation

## MongoDB local installation (Linux)

First, install MongoDB locally using the commands:

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

```bash
sudo apt-get install -y mongodb-org
```

Use this command to start mongoDB.

```bash
sudo systemctl start mongod
```

## Installing Dependencies

Install the required libraries using the command 

`pip install fastapi uvicorn models pydantic database auth bson dotenv`

## Setting up the Environment Variables

Create a `.env` file with the following contents:

```
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017
```

# Running the API

To run the API, use the command `uvicorn main:app --reload`.

The API will start running on `http://127.0.0.1:8000/jobs/`

You can visit `http://127.0.0.1:8000/docs` to view the interactive API documentation (Swagger UI).

# Endpoints Description

The following endpoints are available:

- `POST /signup`: Register a new user account.
- `POST /token`: Logs in a user and generates a JWT token.
- `GET /jobs/`: Retrieve all job records.
- `POST /jobs/`: Create a new job record.
- `GET /jobs/{job_id}`: Retrieve a job record by ID.
- `PUT /jobs/{job_id}`: Update a job record by ID.
- `DELETE /jobs/{job_id}`: Delete a job record by ID.
- `PATCH /jobs/{job_id}`: Partially update a job record by ID.

## Authentication

### Sign Up (User registration)

This registers a new user account.

```
POST /signup
```

- Register a new user account.
- **Request Body**:

  ```json
  {
    "username": "your_username",
    "password": "string"
  }
  ```

- **Example**:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/signup' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser",
  "password": "testpassword"
}'
```

### Log In (User login)

```
POST /token
```

- Logs in a user and generates a JWT token.
- **Request body**:

  ```json
  {
    "username": "your_username",
    "password": "string"
  }
  ```

- **Response**:

  ```json
  {
    "access_token": "your_access_token",
    "token_type": "bearer"
  }
  ```

- **Example**:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=testuser&password=testpassword'
```

Store the access token generated here. This will be needed for future API requests.

## Job Postings

### Create a Job Posting

```
POST /jobs/
```

- **Authorization**: Requires Bearer Token (Created while signing up)
- **Request body**:

```json
{
  "job_title": "Software Engineer",
  "job_description": "Develop and maintain software applications.",
  "skills_required": ["Python", "FastAPI", "MongoDB"],
  "qualifications": "Bachelors degree in Computer Science",
  "company_name": "AkshitGureja",
  "location": "Remote",
  "job_type": "full-time",
  "salary": 150000,
  "id": "66e837f1c615e331a2f79d68"
}
```

- Example request (using terminal):

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/jobs/' \
  -H 'Authorization: Bearer your_access_token_here' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_title": "Software Engineer",
  "job_description": "Develop and maintain software applications.",
  "skills_required": ["Python", "FastAPI", "MongoDB"],
  "qualifications": "Bachelor''s degree in Computer Science",
  "company_name": "Company",
  "location": "Remote",
  "job_type": "full-time",
  "salary": 120000
}'
```

### Retrieve all Job Postings

```
GET /jobs/
```

- Retrieves a list of all job postings.
- **Response**:

```json
[
  {
    "id": "64f6a2e9d42b6b1e7e07d69f",
    "job_title": "Software Engineer",
    "job_description": "Develop and maintain software...",
    "skills_required": ["Python", "FastAPI"],
    "qualifications": "Bachelor's in Computer Science",
    "company_name": "NewCompany",
    "location": "New York, NY",
    "job_type": "full-time",
    "salary": 120000
  }
]
```

- Example request (using terminal):

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/jobs/'
```

### Retrieve a Specific Job by ID

```
GET /jobs/{job_id}
```

- Retrieves the details of a specific job posting by its ID.
- **Response**:

```json
{
  "id": "64f6a2e9d42b6b1e7e07d69f",
  "job_title": "Software Engineer",
  "job_description": "Develop and maintain software...",
  "skills_required": ["Python", "FastAPI"],
  "qualifications": "Bachelor's in Computer Science",
  "company_name": "TechCorp",
  "location": "New York, NY",
  "job_type": "full-time",
  "salary": 120000
}
```

- Example request (using terminal):

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/jobs/{job_id}' \
  -H 'Authorization: Bearer your_access_token_here'
```

### Update a Job Posting (Full Update)

```
PUT /jobs/{job_id}
```

- **Authorization**: Requires Bearer Token.
- **Request body**: Same as the create request.
- **Response**: The updated job posting.
- Example request (using terminal):

```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/jobs/{job_id}' \
  -H 'Authorization: Bearer your_access_token_here' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_title": "Software Engineer",
  "job_description": "Develop and maintain software applications.",
  "skills_required": ["Python", "FastAPI", "MongoDB"],
  "qualifications": "Bachelor''s degree in Computer Science",
  "company_name": "Company",
  "location": "Remote",
  "job_type": "full-time",
  "salary": 130000
}'
```

### Update a Job Posting (Partial Update)

```
PATCH /jobs/{job_id}
```

- **Authorization**: Requires Bearer Token.
- **Request body**: Only the fields to be updated.

```json
{
  "salary": 130000
}
```

- **Response**: The updated job posting.
- Example request (using terminal):

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/jobs/{job_id}' \
  -H 'Authorization: Bearer your_access_token_here' \
  -H 'Content-Type: application/json' \
  -d '{
  "salary": 130000
}'
```

### Delete a Job Posting

```
DELETE /jobs/{job_id}
```

- **Authorization**: Requires Bearer Token.
- **Response**:

```json
{
  "msg": "Job deleted successfully"
}
```

- Example request (using terminal):

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/jobs/{job_id}' \
  -H 'Authorization: Bearer your_access_token_here'
```
