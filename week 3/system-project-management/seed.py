from datetime import datetime, timedelta, timezone

from app.auth.security import get_password_hash
from app.database import SessionLocal, engine
from app.models import project, task, user

UTC = timezone.utc
DEFAULT_PASSWORD = "password123"


def dt(days_offset: int) -> datetime:
    return datetime.now(UTC) + timedelta(days=days_offset)


def seed_data() -> None:
    user.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(user.User).first():
            print("The database already has data. Skipping seeding.")
            return

        print("Adding richer sample data...")

        users_data = [
            {"username": "manager1", "email": "manager@test.com", "role": "manager", "is_active": True},
            {"username": "sara.ali", "email": "sara.ali@test.com", "role": "employee", "is_active": True},
            {"username": "ahmed.dev", "email": "ahmed.dev@test.com", "role": "employee", "is_active": True},
            {"username": "noor.ui", "email": "noor.ui@test.com", "role": "employee", "is_active": True},
            {"username": "khaled.qa", "email": "khaled.qa@test.com", "role": "employee", "is_active": True},
            {"username": "mariam.pm", "email": "mariam.pm@test.com", "role": "employee", "is_active": True},
        ]

        created_users: dict[str, user.User] = {}
        for item in users_data:
            db_user = user.User(
                username=item["username"],
                email=item["email"],
                hashed_password=get_password_hash(DEFAULT_PASSWORD),
                role=item["role"],
                is_active=item["is_active"],
            )
            db.add(db_user)
            db.flush()
            created_users[item["username"]] = db_user

        manager = created_users["manager1"]

        projects_data = [
            {
                "title": "Website Redesign",
                "description": "Refresh the public website with a cleaner landing page, updated navigation, and better mobile responsiveness.",
                "status": "active",
            },
            {
                "title": "Mobile App MVP",
                "description": "Build the first internal mobile MVP for task tracking, login, and dashboard access.",
                "status": "planned",
            },
            {
                "title": "Inventory Dashboard",
                "description": "Create an internal dashboard for stock levels, item trends, and low inventory alerts.",
                "status": "active",
            },
            {
                "title": "Customer Support Portal",
                "description": "Develop a lightweight portal for ticket management, updates, and support team reporting.",
                "status": "completed",
            },
            {
                "title": "HR Attendance System",
                "description": "Implement attendance check-in, approval, and reporting screens for internal HR workflows.",
                "status": "active",
            },
            {
                "title": "Internal Admin Panel",
                "description": "Provide user management, settings, and permissions management for staff operations.",
                "status": "planned",
            },
        ]

        created_projects: dict[str, project.Project] = {}
        for item in projects_data:
            db_project = project.Project(
                title=item["title"],
                description=item["description"],
                status=item["status"],
                owner_id=manager.id,
            )
            db.add(db_project)
            db.flush()
            created_projects[item["title"]] = db_project

        tasks_data = [
            # Website Redesign
            {
                "project": "Website Redesign",
                "title": "Design login screen",
                "description": "Prepare a clean desktop-first login page layout and form spacing.",
                "status": "completed",
                "priority": "high",
                "due_date": dt(-10),
                "assigned_to": "noor.ui",
            },
            {
                "project": "Website Redesign",
                "title": "Build responsive navbar",
                "description": "Implement responsive top navigation and improve active state styling.",
                "status": "in_progress",
                "priority": "medium",
                "due_date": dt(3),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "Website Redesign",
                "title": "Fix dashboard spacing",
                "description": "Adjust dashboard cards and table spacing to improve visual hierarchy.",
                "status": "todo",
                "priority": "medium",
                "due_date": dt(6),
                "assigned_to": "sara.ali",
            },
            {
                "project": "Website Redesign",
                "title": "QA homepage flow",
                "description": "Test homepage links, hero sections, and navigation across common screen sizes.",
                "status": "todo",
                "priority": "low",
                "due_date": dt(8),
                "assigned_to": "khaled.qa",
            },
            # Mobile App MVP
            {
                "project": "Mobile App MVP",
                "title": "Define MVP feature list",
                "description": "Finalize the first release scope for login, tasks, and summary widgets.",
                "status": "completed",
                "priority": "high",
                "due_date": dt(-4),
                "assigned_to": "mariam.pm",
            },
            {
                "project": "Mobile App MVP",
                "title": "Create API integration plan",
                "description": "Document required endpoints and payload formats for mobile integration.",
                "status": "in_progress",
                "priority": "high",
                "due_date": dt(5),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "Mobile App MVP",
                "title": "Design task list mockups",
                "description": "Create a simple mobile UI concept for the employee task list experience.",
                "status": "todo",
                "priority": "medium",
                "due_date": dt(9),
                "assigned_to": "noor.ui",
            },
            # Inventory Dashboard
            {
                "project": "Inventory Dashboard",
                "title": "Build stock summary API",
                "description": "Create the backend endpoint for inventory totals and warning counts.",
                "status": "in_progress",
                "priority": "high",
                "due_date": dt(2),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "Inventory Dashboard",
                "title": "Create dashboard seed data",
                "description": "Add enough records so inventory widgets and tables look populated.",
                "status": "completed",
                "priority": "medium",
                "due_date": dt(-7),
                "assigned_to": "sara.ali",
            },
            {
                "project": "Inventory Dashboard",
                "title": "Add chart placeholder cards",
                "description": "Prepare simple UI blocks for future analytics without adding a chart library.",
                "status": "todo",
                "priority": "low",
                "due_date": dt(12),
                "assigned_to": "noor.ui",
            },
            {
                "project": "Inventory Dashboard",
                "title": "Regression test filters",
                "description": "Verify table filtering and sorting behavior after layout changes.",
                "status": "todo",
                "priority": "medium",
                "due_date": dt(1),
                "assigned_to": "khaled.qa",
            },
            # Customer Support Portal
            {
                "project": "Customer Support Portal",
                "title": "Implement ticket list page",
                "description": "Create the main support ticket table and status indicators.",
                "status": "completed",
                "priority": "high",
                "due_date": dt(-20),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "Customer Support Portal",
                "title": "Validate ticket form",
                "description": "Ensure required fields and error messages are displayed correctly.",
                "status": "completed",
                "priority": "medium",
                "due_date": dt(-18),
                "assigned_to": "sara.ali",
            },
            {
                "project": "Customer Support Portal",
                "title": "Finalize support roles",
                "description": "Review role permissions for manager and employee support users.",
                "status": "completed",
                "priority": "medium",
                "due_date": dt(-14),
                "assigned_to": "mariam.pm",
            },
            # HR Attendance System
            {
                "project": "HR Attendance System",
                "title": "Build attendance table",
                "description": "Create the main attendance list screen with simple daily summaries.",
                "status": "in_progress",
                "priority": "high",
                "due_date": dt(4),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "HR Attendance System",
                "title": "Design employee check-in form",
                "description": "Prepare a compact check-in/check-out UI for desktop users.",
                "status": "in_progress",
                "priority": "medium",
                "due_date": dt(7),
                "assigned_to": "noor.ui",
            },
            {
                "project": "HR Attendance System",
                "title": "Write approval workflow notes",
                "description": "Document the manager review flow for attendance corrections.",
                "status": "todo",
                "priority": "low",
                "due_date": dt(10),
                "assigned_to": "mariam.pm",
            },
            {
                "project": "HR Attendance System",
                "title": "Test employee permissions",
                "description": "Verify employees only see their own attendance-related actions.",
                "status": "todo",
                "priority": "high",
                "due_date": dt(-1),
                "assigned_to": "khaled.qa",
            },
            # Internal Admin Panel
            {
                "project": "Internal Admin Panel",
                "title": "Create users table page",
                "description": "Build a user management page with role and active status badges.",
                "status": "completed",
                "priority": "high",
                "due_date": dt(-6),
                "assigned_to": "sara.ali",
            },
            {
                "project": "Internal Admin Panel",
                "title": "Add role badges",
                "description": "Style manager and employee badges with consistent color usage.",
                "status": "completed",
                "priority": "medium",
                "due_date": dt(-5),
                "assigned_to": "noor.ui",
            },
            {
                "project": "Internal Admin Panel",
                "title": "Implement logout flow",
                "description": "Ensure logout clears local state and redirects users correctly.",
                "status": "in_progress",
                "priority": "medium",
                "due_date": dt(2),
                "assigned_to": "ahmed.dev",
            },
            {
                "project": "Internal Admin Panel",
                "title": "Review inactive user handling",
                "description": "Confirm inactive accounts cannot continue using protected pages.",
                "status": "todo",
                "priority": "medium",
                "due_date": dt(11),
                "assigned_to": "khaled.qa",
            },
            {
                "project": "Internal Admin Panel",
                "title": "Prepare final presentation demo",
                "description": "Review seeded data and ensure all main manager screens look populated.",
                "status": "todo",
                "priority": "high",
                "due_date": dt(14),
                "assigned_to": "mariam.pm",
            },
        ]

        for item in tasks_data:
            db_task = task.Task(
                title=item["title"],
                description=item["description"],
                status=item["status"],
                priority=item["priority"],
                due_date=item["due_date"],
                project_id=created_projects[item["project"]].id,
                assigned_to=created_users[item["assigned_to"]].id,
                created_by=manager.id,
            )
            db.add(db_task)

        db.commit()

        print("✅ Rich sample data added successfully!")
        print(f"Users created: {len(users_data)}")
        print(f"Projects created: {len(projects_data)}")
        print(f"Tasks created: {len(tasks_data)}")
        print(f"Default password for all seeded users: {DEFAULT_PASSWORD}")
        print("Manager account: username: manager1 | password: password123")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
