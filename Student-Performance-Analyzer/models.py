class Student:
    def __init__(self, name: str, student_id: str, grades: list = None):
        # التحقق من صحة المدخلات الأساسية
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if not student_id.strip().isalnum():
            raise ValueError("Student ID must be alphanumeric.")

        # تطبيق التغليف (Encapsulation)
        self.__name = name.strip()
        self.__student_id = student_id.strip()
        self.__grades = []
        
        if grades:
            for g in grades:
                self.add_grade(g)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def student_id(self) -> str:
        return self.__student_id

    @property
    def grades(self) -> list:
        return self.__grades.copy()

    def add_grade(self, grade: float):
        if 0 <= grade <= 100:
            self.__grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100.")

    def calculate_average(self) -> float:
        if len(self.__grades) == 0:
            return 0.0
        return sum(self.__grades) / len(self.__grades)

    def get_grade_category(self) -> str:
        if len(self.__grades) == 0:
            return 'N/A'
        
        avg = self.calculate_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'

    @classmethod
    def from_dict(cls, data: dict):
        """إنشاء كائن طالب من قاموس (مثل البيانات القادمة من CSV)"""
        name = data.get('name', '').strip()
        student_id = data.get('student_id', '').strip()
        
        grades_str = data.get('grades', '').strip()
        grades = []
        if grades_str:
            grades = [float(g.strip()) for g in grades_str.split(',') if g.strip()]

        return cls(name, student_id, grades)


class Classroom:
    def __init__(self):
        self.__students = []

    def get_all_students(self) -> list:
        return self.__students

    def add_student(self, student: Student):
        if self.search_student(student.student_id):
            raise ValueError(f"Student ID '{student.student_id}' already exists.")
        self.__students.append(student)

    def search_student(self, student_id: str):
        for student in self.__students:
            if student.student_id.lower() == student_id.strip().lower():
                return student
        return None

    def search_student_by_name(self, name: str) -> list:
        search_name = name.strip().lower()
        return [s for s in self.__students if s.name.lower() == search_name]

    def remove_student(self, student_id: str) -> bool:
        student = self.search_student(student_id)
        if student:
            self.__students.remove(student)
            return True
        return False

    def calculate_classroom_average(self) -> float:
        if len(self.__students) == 0:
            return 0.0
        total = sum(s.calculate_average() for s in self.__students)
        return total / len(self.__students)