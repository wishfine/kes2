# teaching_plan_table.py
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from collections import defaultdict
from course import Course

class TeachingPlanTable(QWidget):
    def __init__(self, teaching_plan):
        super().__init__()

        self.teaching_plan = teaching_plan

        self.init_ui()

    def init_ui(self):
        table = QTableWidget(self)
        table.setColumnCount(3)  # Assuming three columns: Course Name, Credits, Semester

        headers = ["课程名称", "学分", "学期"]
        table.setHorizontalHeaderLabels(headers)

        row = 0
        for semester, courses in self.teaching_plan.items():
            for course in courses:
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(course.course_name))
                table.setItem(row, 1, QTableWidgetItem(str(course.credits)))
                table.setItem(row, 2, QTableWidgetItem(str(course.semester)))
                row += 1

        table.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addWidget(table)

        self.setLayout(layout)
        self.setWindowTitle("课程教学计划表格")
        self.setGeometry(600, 600, 600, 400)
