import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QComboBox, \
    QScrollArea, QTextBrowser, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from collections import defaultdict
import re
import graphviz


class Course:
    def __init__(self, course_name, credits, prereqs):
        self.course_name = course_name
        self.credits = credits
        self.prereqs = prereqs
        self.semester = 0


class TeachingPlanGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.input_filename = QLineEdit(self)
        self.output_filename = QLineEdit(self)
        self.generate_mode_combo = QComboBox(self)
        self.generate_mode_combo.addItems(["尽快修完所有课程", "每学期学习负担尽可能相同"])

        browse_input_button = QPushButton("浏览", self)
        browse_output_button = QPushButton("浏览", self)

        browse_input_button.clicked.connect(self.browse_input_file)
        browse_output_button.clicked.connect(self.browse_output_file)

        generate_button = QPushButton("生成教学计划", self)
        generate_button.clicked.connect(self.generate_plan)

        generate_graph_button = QPushButton("生成有向图", self)
        generate_graph_button.clicked.connect(self.generate_graph)

        show_table_button = QPushButton("显示课表", self)
        show_table_button.clicked.connect(self.show_table)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("输入文件："))
        layout.addWidget(self.input_filename)
        layout.addWidget(browse_input_button)
        layout.addWidget(QLabel("输出文件："))
        layout.addWidget(self.output_filename)
        layout.addWidget(browse_output_button)
        layout.addWidget(QLabel("生成方式:"))
        layout.addWidget(self.generate_mode_combo)
        self.generate_mode_combo.setFixedWidth(600)
        self.generate_mode_combo.setFixedHeight(60)
        layout.addWidget(generate_button)
        layout.addWidget(generate_graph_button)
        layout.addWidget(show_table_button)

        self.setLayout(layout)
        self.setWindowTitle("课程教学计划生成器")
        self.setGeometry(600, 600, 800, 600)

        # Variables to store teaching plan for later display
        self.teaching_plan = None

    def browse_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择输入文件", "", "Text Files (*.txt)")
        self.input_filename.setText(filename)

    def browse_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "选择输出文件", "", "Text Files (*.txt)")
        self.output_filename.setText(filename)

    def generate_plan(self):
        input_file = self.input_filename.text()
        output_file = self.output_filename.text()
        plan_type = self.generate_mode_combo.currentText()

        if not input_file or not output_file:
            QMessageBox.critical(self, "错误", "请输入输入和输出文件名。")
            return

        try:
            semester_count, max_credits_per_semester, course_info, course_graph = read_input_file(input_file)

            if semester_count is not None:
                topological_order = topological_sort(course_graph)

                if plan_type == "尽快修完所有课程":
                    teaching_plan, semester_credits, course_semesters = generate_teaching_plan(topological_order,
                                                                                                max_credits_per_semester,
                                                                                                semester_count,
                                                                                                course_info)
                elif plan_type == "每学期学习负担尽可能相同":
                    teaching_plan, course_semesters = generate_balanced_teaching_plan_v2(topological_order,
                                                                                        max_credits_per_semester,
                                                                                        semester_count,
                                                                                        course_info)

                output_teaching_plan(teaching_plan, course_info, output_file)
                self.teaching_plan = teaching_plan  # Store teaching plan for later display

                QMessageBox.information(self, "成功", "教学计划已生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def generate_graph(self,course_semesters):
        input_file = self.input_filename.text()
        output_file = self.output_filename.text()

        if not input_file or not output_file:
            QMessageBox.critical(self, "错误", "请输入输入和输出文件名。")
            return

        try:
            semester_count, max_credits_per_semester, course_info, course_graph = read_input_file(input_file)

            if semester_count is not None:
                dot = graphviz.Digraph(format='png')

                topological_order = topological_sort(course_graph)
                max_semesters = max(course_semesters.values())

                for semester_number in range(1, max_semesters + 1):
                    courses_in_semester = [course_name for course_name, semester in course_semesters.items() if
                                           semester == semester_number]

                    if semester_number == 1:
                        dot.node(f"Semester {semester_number}\n{', '.join(courses_in_semester)}", shape='box',
                                 style='filled', color='lightblue')
                    else:
                        dot.node(f"Semester {semester_number}\n{', '.join(courses_in_semester)}", shape='box')

                    if semester_number > 1:
                        for course_name in courses_in_semester:
                            for prereq_name in course_info[course_name].prereqs:
                                if course_semesters[prereq_name] < semester_number:
                                    dot.edge(f"Semester {course_semesters[prereq_name]}\n{prereq_name}",
                                             f"Semester {semester_number}\n{course_name}")

                dot.render(output_file, format='png', cleanup=True)
                QMessageBox.information(self, "成功", "有向图已生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def show_table(self):
        if self.teaching_plan is not None:
            self.table_window = TeachingPlanTable(self.teaching_plan)
            self.table_window.show()


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



def read_input_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            semester_count, max_credits_per_semester = map(int, re.findall(r'\d+', file.readline()))
            course_graph = defaultdict(list)
            course_info = {}

            for line in file:
                items = line.strip().split('\t')
                course_name = items[0]
                credits = float(items[1])
                prereq = [] if items[2] == '-' else items[2].split('，')

                course = Course(course_name, credits, prereq)
                course_info[course_name] = course

                for prereq_name in prereq:
                    course_graph[prereq_name].append(course_name)

            return semester_count, max_credits_per_semester, course_info, course_graph
    except FileNotFoundError:
        raise Exception("找不到输入文件。")
    except ValueError:
        raise Exception("输入格式错误。请检查输入文件。")


def topological_sort(course_graph):
    in_degree = defaultdict(int)
    for node in course_graph:
        for neighbor in course_graph[node]:
            in_degree[neighbor] += 1

    current_stack = []
    backup_stack = []

    for node in course_graph:
        if in_degree[node] == 0:
            current_stack.append(node)

    topological_order = []

    while current_stack or backup_stack:
        while current_stack:
            node = current_stack.pop()
            topological_order.append(node)

            for neighbor in course_graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    backup_stack.append(neighbor)

        current_stack, backup_stack = backup_stack, current_stack

    return topological_order


def generate_teaching_plan(topological_order, max_credits_per_semester, max_semesters, course_info):
    semester_number = 1
    semester_credits = defaultdict(float)
    course_semesters = {}
    teaching_plan = defaultdict(list)

    for course_name in topological_order:
        course = course_info[course_name]
        prereq_semesters = [course_semesters.get(prereq_name, 0) for prereq_name in course.prereqs]

        if prereq_semesters and max(prereq_semesters) == semester_number:
            semester_number += 1
            semester_credits[semester_number] = 0

        if semester_number > max_semesters:
            raise Exception("无法满足学分限制和课程先修条件。")

        course.semester = semester_number
        teaching_plan[semester_number].append(course)
        semester_credits[semester_number] += course.credits
        course_semesters[course_name] = semester_number

    return teaching_plan, semester_credits, course_semesters


def generate_balanced_teaching_plan_v2(topological_order, max_credits_per_semester, max_semesters, course_info):
    semester_number = 1
    course_semesters = {}
    remaining_credits = defaultdict(float)
    teaching_plan = defaultdict(list)

    for course_name in topological_order:
        course = course_info[course_name]
        prereq_semesters = [course_semesters.get(prereq_name, 0) for prereq_name in course.prereqs]

        while semester_number <= max_semesters:
            if prereq_semesters and max(prereq_semesters) == semester_number:
                semester_number += 1
            else:
                break

        if semester_number > max_semesters:
            raise Exception("无法满足学分限制和课程先修条件。")

        if remaining_credits[semester_number] + course.credits > max_credits_per_semester:
            remaining_credits[semester_number] = 0
            semester_number += 1

        if semester_number > max_semesters:
            raise Exception("无法满足学分限制和课程先修条件。")

        course.semester = semester_number
        teaching_plan[semester_number].append(course)
        remaining_credits[semester_number] += course.credits
        course_semesters[course_name] = semester_number

    return teaching_plan, course_semesters


def output_teaching_plan(teaching_plan, course_info, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        max_semester = max(teaching_plan.keys())
        for semester_number in range(1, max_semester + 1):
            courses = teaching_plan[semester_number]
            file.write(f"学期 {semester_number}:\n")
            file.write(f"所修学分: {sum(course.credits for course in courses):.2f}\n")
            file.write("课程列表:\n")
            for course in courses:
                file.write(f"{course.course_name} - {course.credits} 学分\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeachingPlanGenerator()
    window.show()
    sys.exit(app.exec_())
