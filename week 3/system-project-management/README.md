# 🚀 Project & Task Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-yellow)

A **full-stack Project & Task Management System** built using **FastAPI, PostgreSQL, and vanilla JavaScript**.

This application demonstrates a **realistic role-based workflow** where managers create projects and assign tasks to employees while employees track and update their assigned work.

The project focuses on **clean backend architecture, API design, and role-based access control (RBAC)**.

---

# 📌 Features

## 🔐 Authentication
- Secure login using **JWT tokens**
- Password hashing with **bcrypt**
- Token-based authentication for protected routes

---

## 👥 Role Based Access Control

### Manager
Managers have full system access.

Managers can:
- Create projects
- Update projects
- Delete projects
- Create tasks
- Assign tasks to employees
- View all users
- View all projects and tasks

### Employee
Employees have limited access.

Employees can:
- View projects they are involved in
- View tasks assigned to them
- Update task status
- Track progress of assigned tasks

---

# 📊 Application Modules

## 📂 Project Management

Managers can:
- Create projects
- Update project details
- Delete projects
- View project status

Projects are displayed in a **card-based UI layout** for easy navigation.

---

## 📋 Task Management

Managers can:
- Create tasks
- Assign tasks to employees
- Set task status
- Manage project tasks

Each task includes:
- Title
- Description
- Assigned employee
- Status
- Related project

---

## 📑 My Tasks Page

Employees have a dedicated page where they can:
- View their assigned tasks
- Track task progress
- Update task status

---

# 🏗 System Architecture

```
Frontend (HTML + JavaScript)
          │
          ▼
FastAPI REST API
          │
          ▼
SQLAlchemy ORM
          │
          ▼
PostgreSQL Database
```

The frontend communicates with the backend via **REST API calls** using the **Fetch API**.

---

# ⚙️ Tech Stack

## Backend

| Technology | Purpose |
|------------|--------|
FastAPI | Backend API framework |
SQLAlchemy | ORM |
Pydantic | Data validation |
PostgreSQL | Database |
JWT | Authentication |
Uvicorn | ASGI server |

---

## Frontend

| Technology | Purpose |
|------------|--------|
HTML5 | Page structure |
CSS3 | Styling |
JavaScript (ES6+) | Dynamic functionality |
Fetch API | API communication |

---

# 📁 Project Structure

```
project-management-system
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── database.py
│
│   ├── auth
│   │   ├── jwt.py
│   │   ├── security.py
│   │   └── deps.py
│
│   ├── models
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│
│   ├── schemas
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│
│   ├── crud
│   │   ├── users.py
│   │   ├── projects.py
│   │   └── tasks.py
│
│   └── routers
│       ├── auth.py
│       ├── users.py
│       ├── projects.py
│       └── tasks.py
│
├── frontend
│   ├── login.html
│   ├── dashboard.html
│   ├── projects.html
│   ├── project-details.html
│   ├── my-tasks.html
│   ├── css
│   └── js
│
├── seed.py
├── requirements.txt
└── README.md
```

---

# 📚 API Documentation

FastAPI automatically provides documentation.

After running the server open:

```
http://127.0.0.1:8000/docs
```

or

```
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Overview

## Auth

```
POST /auth/register
POST /auth/login
GET /auth/me
```

---

## Users

```
GET /users
GET /users/{id}
PUT /users/{id}
DELETE /users/{id}
```

Manager access only.

---

## Projects

```
GET /projects
POST /projects
GET /projects/{id}
PUT /projects/{id}
DELETE /projects/{id}
```

---

## Tasks

```
GET /tasks
POST /tasks
GET /tasks/{id}
PUT /tasks/{id}
DELETE /tasks/{id}
```

---

# 🚀 Running the Project

## 1️⃣ Clone Repository

```
git clone <repository-url>
cd project-management-system
```

---

# 🐍 Backend Setup

## Create Virtual Environment

Windows

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux

```
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/project_management
JWT_SECRET_KEY=your-secret-key
```

---

## Run Database Seed

```
python seed.py
```

This creates demo accounts.

### Manager

```
username: manager1
password: password123
```

### Employee

```
username: ahmed.dev
password: password123
```

---

## Run Backend Server

```
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

# 🌐 Frontend Setup

Navigate to the frontend folder:

```
cd frontend
python -m http.server 5500
```

Open:

```
http://localhost:5500
```

---


# 🧠 Development Notes

### Authorization Header

All protected requests require:

```
Authorization: Bearer <JWT_TOKEN>
```

---

### Cache Issues

If frontend changes do not appear:

- Hard refresh browser
- Clear browser cache

---

### CORS Warning

Opening HTML files using `file://` may cause API errors.

Always run frontend using a **local server**.