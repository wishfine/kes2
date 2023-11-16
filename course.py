# course.py
class Course:
    def __init__(self, course_name, credits, prereqs):
        self.course_name = course_name
        self.credits = credits
        self.prereqs = prereqs
        self.semester = 0
