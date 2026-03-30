# 🚀 Week 3: Full-Stack API Development & Database Integration

Welcome to the **Week 3** repository of the Data Engineering Bootcamp. This week marks a significant milestone as we transition into building robust, scalable backend architectures and integrating them with frontend interfaces. 

This directory serves as a showcase of building a complete, secure, and fully functional web application from scratch.

---

## 📂 Project Showcase

### 🛠️ Project Management System (`system-project-management`)
A comprehensive full-stack application designed to manage users, projects, and tasks with role-based access control.
- **Objective:** Develop a secure RESTful API using FastAPI, manage relational data using SQLAlchemy ORM, and connect it to a dynamic vanilla JavaScript frontend.
- **Highlighted Skills:** - **Backend Development:** REST API design, routing, and CRUD operations using FastAPI.
  - **Database Management:** SQLAlchemy ORM, database seeding (`seed.py`), and schema validation using Pydantic.
  - **Security:** JWT (JSON Web Tokens) authentication, password hashing, and secure route dependencies.
  - **Frontend Integration:** Consuming APIs using asynchronous JavaScript (Fetch API) and dynamic DOM manipulation.
- **Tech Stack:** Python, FastAPI, SQLAlchemy, SQLite/PostgreSQL, HTML, CSS, Vanilla JavaScript.

---

## 🏗️ Architecture Overview
The backend follows a clean, modular architecture:
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic models for data validation.
- `app/crud/`: Database interaction logic.
- `app/routers/`: API endpoints grouped by functionality.
- `app/auth/`: Security and JWT token management.
- `frontend/`: Client-side interface for users and managers. Build by using AI

---
*Navigate to the `system-project-management` folder to view the source code, setup instructions, and the complete application structure.*