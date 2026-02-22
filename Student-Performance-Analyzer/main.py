from models import Classroom, Student
import analytics
import utils

def display_menu():
    print("\n" + "="*45)
    print("      STUDENT PERFORMANCE ANALYZER")
    print("="*45)
    print(" 1. Add a New Student & Grades")
    print(" 2. Add a Grade to an Existing Student")
    print(" 3. Remove a Student")
    print(" 4. Search for a Student")
    print(" 5. View Classroom Analytics & Rankings")
    print(" 6. Save and Exit")
    print("-" * 45)

def main():
    classroom = Classroom()
    file_path = 'data.csv'
    
    # تحميل البيانات السابقة إن وجدت
    utils.load_students_from_csv(file_path, classroom)

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == '1':
                print("\n--- Add New Student ---")
                name = input("Enter student name: ").strip()
                student_id = input("Enter student ID: ").strip()
                
                if not name or not utils.validate_id(student_id):
                    print("[-] Error: Invalid name or ID.")
                    continue

                try:
                    student = Student(name, student_id)
                    classroom.add_student(student)
                    print(f"[+] Student '{name}' added successfully.")
                except ValueError as e:
                    print(f"[-] Error: {e}")
                    continue

                print("Enter grades below (type 'done' when finished):")
                while True:
                    grade_input = input(" -> Grade: ").strip()
                    if grade_input.lower() == 'done':
                        break
                    try:
                        grade = float(grade_input)
                        student.add_grade(grade)
                        print(f"    [+] Added {grade}")
                    except ValueError:
                        print("    [-] Error: Please enter a valid number.")

            elif choice == '2':
                print("\n--- Add Grade ---")
                student_id = input("Enter student ID: ").strip()
                student = classroom.search_student(student_id)
                
                if student:
                    grade_str = input(f"Enter new grade for {student.name}: ").strip()
                    try:
                        student.add_grade(float(grade_str))
                        print("[+] Grade added successfully.")
                    except ValueError:
                        print("[-] Error: Invalid grade number.")
                else:
                    print("[-] Student not found.")

            elif choice == '3':
                print("\n--- Remove Student ---")
                student_id = input("Enter student ID to remove: ").strip()
                student = classroom.search_student(student_id)
                
                if student:
                    confirm = input(f"Are you sure you want to remove {student.name}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        classroom.remove_student(student_id)
                        print("[+] Student removed successfully.")
                    else:
                        print("[i] Operation cancelled.")
                else:
                    print("[-] Student not found.")

            elif choice == '4':
                print("\n--- Search Student ---")
                print("1. Search by ID")
                print("2. Search by Name")
                search_choice = input("Select search method (1 or 2): ").strip()
                
                found_students = []
                if search_choice == '1':
                    student_id = input("Enter student ID: ").strip()
                    student = classroom.search_student(student_id)
                    if student: found_students.append(student)
                elif search_choice == '2':
                    name = input("Enter student name: ").strip()
                    found_students = classroom.search_student_by_name(name)
                else:
                    print("[-] Invalid choice.")
                    continue
                
                if found_students:
                    for s in found_students:
                        print(f"\n--- Result ---")
                        print(f"Name:    {s.name}")
                        print(f"ID:      {s.student_id}")
                        print(f"Average: {s.calculate_average():.2f}")
                        print(f"Grade:   {s.get_grade_category()}")
                        print(f"Grades:  {s.grades}")
                else:
                    print("[-] No matching student found.")

            elif choice == '5':
                if not classroom.get_all_students():
                    print("[i] Classroom is empty.")
                    continue
                
                print("\n=== CLASSROOM ANALYTICS ===")
                print(f"Overall Average: {classroom.calculate_classroom_average():.2f}")
                
                top = analytics.get_top_performing_student(classroom)
                low = analytics.get_lowest_performing_student(classroom)
                if top: print(f"Top Student:     {top.name} (Avg: {top.calculate_average():.2f})")
                if low: print(f"Lowest Student:  {low.name} (Avg: {low.calculate_average():.2f})")
                
                print("\nGrade Distribution:")
                dist = analytics.get_grade_distribution(classroom)
                for grade, count in dist.items():
                    print(f"  {grade}: {count} students")
                    
                print("\nRankings:")
                ranked = analytics.rank_students(classroom)
                for i, s in enumerate(ranked, 1):
                    print(f"  {i}. {s.name} | ID: {s.student_id} | Avg: {s.calculate_average():.2f}")

            elif choice == '6':
                utils.save_students_to_csv(file_path, classroom)
                print("\n[+] Data saved successfully!")
                print("Exiting system. Goodbye!")
                break

            else:
                print("[-] Invalid choice. Please try again.")

        except Exception as e:
            print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()