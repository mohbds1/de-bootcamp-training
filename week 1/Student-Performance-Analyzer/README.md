<h1 align="center">🎓 Student Performance Analyzer</h1>

<p align="center">
  A command-line system for managing students, tracking grades, and generating performance analytics — built with clean OOP architecture in pure Python.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/storage-CSV-green?style=for-the-badge" alt="CSV Storage">
  <img src="https://img.shields.io/badge/interface-CLI-orange?style=for-the-badge" alt="CLI Interface">
  <img src="https://img.shields.io/badge/license-MIT-purple?style=for-the-badge" alt="MIT License">
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Architecture & Design](#-architecture--design)
- [Technical Highlights](#-technical-highlights)
- [Grade Scale](#-grade-scale)
- [Data Format](#-data-format)
- [License](#-license)

---

## 🔍 Overview

The **Student Performance Analyzer** is a modular, menu-driven CLI application that enables educators to manage student records, track individual grades, and generate comprehensive classroom‑level analytics. The system persists all data to a CSV file automatically.

The project demonstrates professional software engineering practices including:

- **Object-Oriented Programming** with full encapsulation
- **Defensive programming** against corrupt/malformed data
- **Layered architecture** separating models, analytics, utilities, and UI
- **Robust error handling** with user-friendly feedback

---

## ✨ Features

| # | Feature | Description |
|:-:|---------|-------------|
| 1 | **Add Students & Grades** | Register a new student with an alphanumeric ID and interactively enter grades (0–100). |
| 2 | **Add Grades** | Append individual grades to any existing student by ID. |
| 3 | **Remove Students** | Remove a student record by ID with confirmation prompt before deletion. |
| 4 | **Search Students** | Look up any student by **ID** (case-insensitive) or by **Name**, and view their full profile: name, average, grade category, and grade history. |
| 5 | **Classroom Analytics** | View real-time analytics including classroom average, top & lowest performers, grade distribution, and ranked student leaderboard. |
| 6 | **Persistent Storage** | All data is saved to and loaded from `data.csv` automatically on startup and on exit. |

---

## 📁 Project Structure

```
Student-Performance-Analyzer/
│
├── models.py        # Data models — Student & Classroom classes
├── analytics.py     # Analytics engine — ranking, distribution, top/lowest
├── utils.py         # I/O utilities — CSV load/save and validation
├── main.py          # Application entry point — CLI menu & user interaction
├── data.csv         # Persistent student data (auto-generated)
└── README.md        # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (no third-party packages required — stdlib only)

### Running the Application

```bash
python main.py
```

---

## 📖 Usage Guide

When you run `python main.py`, you'll see the interactive menu:

```
=============================================
      STUDENT PERFORMANCE ANALYZER
=============================================
 1. Add a New Student & Grades
 2. Add a Grade to an Existing Student
 3. Remove a Student
 4. Search for a Student
 5. View Classroom Analytics & Rankings
 6. Save and Exit
---------------------------------------------
```

### Quick Walkthrough

1. **Add a student** → Enter name, alphanumeric ID, then grades one by one. Type `done` when finished.
2. **Add a grade** → Enter a student's ID and append a new grade.
3. **Remove a student** → Enter the ID, then confirm with `y/n`.
4. **Search** → Choose to search by ID (case-insensitive) or by Name, then view the student's full profile.
5. **View analytics** → See the classroom average, top & lowest performers, grade distribution, and full rankings.
6. **Save & Exit** → Persists all changes to `data.csv`.

---

## 🏗️ Architecture & Design

The system follows a **layered architecture** with clear separation of concerns:

```
┌──────────────────────────────────────────┐
│           APPLICATION LAYER              │
│         main.py (CLI / UI)               │
├──────────────────────────────────────────┤
│          ANALYTICS LAYER                 │
│     analytics.py (Business Logic)        │
├──────────────────────────────────────────┤
│           UTILITY LAYER                  │
│      utils.py (I/O & Validation)         │
├──────────────────────────────────────────┤
│            MODEL LAYER                   │
│   models.py (Student, Classroom OOP)     │
└──────────────────────────────────────────┘
```

### Module Responsibilities

| Module | Role | Key Classes / Functions |
|--------|------|------------------------|
| `models.py` | Core data models with full encapsulation | `Student`, `Classroom` |
| `analytics.py` | Stateless analytics functions | `get_top_performing_student()`, `get_lowest_performing_student()`, `rank_students()`, `get_grade_distribution()` |
| `utils.py` | File I/O and input validation | `load_students_from_csv()`, `save_students_to_csv()`, `validate_id()` |
| `main.py` | Interactive CLI loop and user-facing output | `main()`, `display_menu()` |

---

## 🔧 Technical Highlights

### Object-Oriented Programming

- **Encapsulation** — All `Student` and `Classroom` attributes are name-mangled (`__name`, `__grades`, etc.) and exposed through `@property` accessors.
- **Copy-safe properties** — `Student.grades` returns a shallow copy to prevent external mutation of internal state.
- **`@classmethod` factory** — `Student.from_dict()` constructs instances from CSV row dictionaries with default-value safety.

### Defensive Programming

- **Constructor validation** — `Student.__init__` rejects empty names and non-alphanumeric IDs at the model layer, independent of UI validation.
- **Safe CSV parsing** — `from_dict()` uses `data.get('key', '').strip()` to gracefully handle missing keys from malformed CSV rows.
- **Graceful error handling** — Per-row `try/except` in CSV loading skips corrupt records without aborting, catching `ValueError` exceptions.
- **Case-insensitive search** — `search_student()` and `search_student_by_name()` normalize casing via `.lower()`.
- **Duplicate ID detection** — Duplicate student IDs are blocked at the `Classroom.add_student()` layer.

### Analytics Engine

- **Ungraded student handling** — Students with no grades receive an `'N/A'` category (not `'F'`) and are excluded from top/lowest performer calculations.
- **Grade distribution** — Tracks `A`, `B`, `C`, `D`, `F`, and `N/A` categories across all students.
- **Ranked leaderboard** — Students are sorted by average in descending order.

---

## 📊 Grade Scale

| Grade | Range |
|:-----:|:-----:|
| A | 90 – 100 |
| B | 80 – 89 |
| C | 70 – 79 |
| D | 60 – 69 |
| F | 0 – 59 |
| N/A | No grades recorded |

---

## 💾 Data Format

Student records are persisted in `data.csv` with the following schema:

```csv
name,student_id,grades
Mohammed Nasser,M1,"90.54,96.2,85.23,90.0,94.5,80.0,86.2"
Ali Hassan,A1,"75.0,82.5,68.0"
```

| Column | Type | Description |
|--------|------|-------------|
| `name` | string | Full student name |
| `student_id` | string | Unique alphanumeric identifier |
| `grades` | string | Comma-separated list of floats (0–100) |

---

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

<p align="center">
  Built with ❤️ using pure Python · No external dependencies
</p>
