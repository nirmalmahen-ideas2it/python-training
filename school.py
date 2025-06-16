from dataclasses import dataclass
from typing import Optional 
from abc import ABC,abstractmethod


class ReportCard(ABC):
    @abstractmethod
    def getReport(self):
        pass

@dataclass
class Person:
    name: Optional[str]=None
    age: Optional[int]=None
    dob: Optional[str]=None
    address: Optional[str]=None
    contact: Optional[str]=None

@dataclass
class StudentMarks():
    english: Optional[int]=None
    maths: Optional[int]=None
    science: Optional[int]=None
    social: Optional[int]=None
    tamil: Optional[int]=None

@dataclass
class Student(Person, ReportCard):
    student_id: Optional[int]=None
    grade: Optional[int]=None
    __marks: Optional[StudentMarks]=None  # Double underscore for name mangling

    def getType(self):
        return "Student"

    
    def setMarks(self, marks):
        self.__marks = marks
    
    def getReport(self):
        print(f"The Report card for Student {self.name} is as follows: ")
        print(f"English: {self.__marks.english}")
        print(f"Tamil: {self.__marks.tamil}")
        print(f"Maths: {self.__marks.maths}")
        print(f"Science: {self.__marks.science}")
        print(f"Social: {self.__marks.social}")

@dataclass
class Teacher(Person):
    teacher_id: Optional[int]=None
    subjects: Optional[list]=None
    students: Optional[list]=None

    def getType(self):
        return "Teacher"
    
teacher_1 = Teacher(name="Teacher 1", age=58, dob="11/12/1969", address="XXX,YYY,ZZZ", contact="1234567890",
                   teacher_id=1, subjects=["English", "Tamil"], students=[])

marks = StudentMarks(english=90, tamil=89, maths=98, social=90, science=89)
student_1 = Student(name="Student 1", age=10, dob="11/12/2011", address="XXX,YYY,ZZZ", 
                   contact="1234567890", grade="Vth Grade", student_id=1)
student_1.setMarks(marks)  # Use setter method instead of direct assignment

print(teacher_1)
print(teacher_1.getType())

print(student_1)
print(student_1.getType())
student_1.getReport()  # Don't print the return value
# This will raise an AttributeError because __marks is private
# print(student_1.__marks)  # This won't work
# print(student_1.getMarks())  # Use getter method instead
    



