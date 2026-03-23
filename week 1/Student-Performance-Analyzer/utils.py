import csv
import os
from models import Classroom, Student

def load_students_from_csv(filepath: str, classroom: Classroom):
    if not os.path.exists(filepath):
        return
        
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    student = Student.from_dict(row)
                    classroom.add_student(student)
                except ValueError as e:
                    print(f"[!] Warning: Skipped a corrupted row. Reason: {e}")
    except Exception as e:
        print(f"[!] Error loading data from file: {e}")

def save_students_to_csv(filepath: str, classroom: Classroom):
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'student_id', 'grades']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for s in classroom.get_all_students():
                grades_str = ','.join(map(str, s.grades))
                writer.writerow({
                    'name': s.name,
                    'student_id': s.student_id,
                    'grades': grades_str
                })
    except Exception as e:
        print(f"[!] Error saving data to file: {e}")

def validate_id(student_id: str) -> bool:
    return student_id.isalnum()