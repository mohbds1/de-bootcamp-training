from models import Classroom, Student

def get_top_performing_student(classroom: Classroom):
    graded_students = [s for s in classroom.get_all_students() if s.grades]
    if not graded_students: 
        return None
    return max(graded_students, key=lambda s: s.calculate_average())

def get_lowest_performing_student(classroom: Classroom):
    graded_students = [s for s in classroom.get_all_students() if s.grades]
    if not graded_students: 
        return None
    return min(graded_students, key=lambda s: s.calculate_average())

def rank_students(classroom: Classroom) -> list:
    return sorted(classroom.get_all_students(), key=lambda s: s.calculate_average(), reverse=True)

def get_grade_distribution(classroom: Classroom) -> dict:
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0, 'N/A': 0}
    for student in classroom.get_all_students():
        grade_cat = student.get_grade_category()
        distribution[grade_cat] += 1
    return distribution