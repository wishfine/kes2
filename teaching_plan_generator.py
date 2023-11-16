# teaching_plan_generator.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QComboBox, \
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout
from collections import defaultdict
import re
import graphviz
from course import Course
from teaching_plan_table import TeachingPlanTable
from utils import read_input_file, topological_sort, generate_teaching_plan, \
    generate_balanced_teaching_plan_v2, output_teaching_plan

class TeachingPlanGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.teaching_plan = None
        self.semester_count = None
        self.max_credits_per_semester = None
        self.course_info = None
        self.course_graph = None

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

        self.modify_course_button = QPushButton("修改课程", self)
        self.modify_course_button.clicked.connect(self.modify_courses)

        self.modify_max_credits_button = QPushButton("修改每学期最大学分限制", self)
        self.modify_max_credits_button.clicked.connect(self.modify_max_credits)

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
        layout.addWidget(self.modify_course_button)
        layout.addWidget(self.modify_max_credits_button)

        self.setLayout(layout)
        self.setWindowTitle("课程教学计划生成器")
        self.setGeometry(600, 600, 800, 600)

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
            self.semester_count, self.max_credits_per_semester, self.course_info, self.course_graph = read_input_file(input_file)

            if self.semester_count is not None:
                topological_order = topological_sort(self.course_graph)

                if plan_type == "尽快修完所有课程":
                    self.teaching_plan, _, _ = generate_teaching_plan(topological_order,
                                                                      self.max_credits_per_semester,
                                                                      self.semester_count,
                                                                      self.course_info)
                elif plan_type == "每学期学习负担尽可能相同":
                    self.teaching_plan, _ = generate_balanced_teaching_plan_v2(topological_order,
                                                                              self.max_credits_per_semester,
                                                                              self.semester_count,
                                                                              self.course_info)

                output_teaching_plan(self.teaching_plan, self.course_info, output_file)

                QMessageBox.information(self, "成功", "教学计划已生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def generate_graph(self):
        input_file = self.input_filename.text()
        output_file = self.output_filename.text()

        if not input_file or not output_file:
            QMessageBox.critical(self, "错误", "请输入输入和输出文件名。")
            return

        try:
            dot = graphviz.Digraph(format='png')

            topological_order = topological_sort(self.course_graph)
            max_semesters = max(self.teaching_plan.values())

            for semester_number in range(1, max_semesters + 1):
                courses_in_semester = [course_name for course_name, semester in self.teaching_plan.items() if
                                       semester == semester_number]

                if semester_number == 1:
                    dot.node(f"Semester {semester_number}\n{', '.join(courses_in_semester)}", shape='box',
                             style='filled', color='lightblue')
                else:
                    dot.node(f"Semester {semester_number}\n{', '.join(courses_in_semester)}", shape='box')

                if semester_number > 1:
                    for course_name in courses_in_semester:
                        for prereq_name in self.course_info[course_name].prereqs:
                            if self.teaching_plan[prereq_name] < semester_number:
                                dot.edge(f"Semester {self.teaching_plan[prereq_name]}\n{prereq_name}",
                                         f"Semester {semester_number}\n{course_name}")

            dot.render(output_file, format='png', cleanup=True)
            QMessageBox.information(self, "成功", "有向图已生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def show_table(self):
        if self.teaching_plan is not None:
            self.table_window = TeachingPlanTable(self.teaching_plan)
            self.table_window.show()

    def modify_courses(self):
        # 弹出课程修改对话框
        dialog = ModifyCoursesDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # 用户点击了“确认”按钮，进行相应的处理
            # 在这里更新课程数据结构，然后重新生成教学计划
            self.generate_new_plan()

    def modify_max_credits(self):
        # 弹出最大学分限制修改对话框
        dialog = ModifyMaxCreditsDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # 用户点击了“确认”按钮，进行相应的处理
            # 在这里更新最大学分限制数据结构，然后重新生成教学计划
            self.generate_new_plan()

    def generate_new_plan(self):
        try:
            topological_order = topological_sort(self.course_graph)

            if self.generate_mode_combo.currentText() == "尽快修完所有课程":
                self.teaching_plan, _, _ = generate_teaching_plan(topological_order,
                                                                  self.max_credits_per_semester,
                                                                  self.semester_count,
                                                                  self.course_info)
            elif self.generate_mode_combo.currentText() == "每学期学习负担尽可能相同":
                self.teaching_plan, _ = generate_balanced_teaching_plan_v2(topological_order,
                                                                          self.max_credits_per_semester,
                                                                          self.semester_count,
                                                                          self.course_info)

            QMessageBox.information(self, "成功", "教学计划已重新生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))


# 新增的部分 - 用于修改课程的对话框
class ModifyCoursesDialog(QDialog):
    def __init__(self, parent=None):
        super(ModifyCoursesDialog, self).__init__(parent)
        self.setWindowTitle("修改课程")
        self.init_ui()

    def init_ui(self):
        # 在这里添加用于修改课程的界面元素
        form_layout = QFormLayout(self)

        # 示例：添加课程名称输入框
        course_name_edit = QLineEdit(self)
        form_layout.addRow("课程名称:", course_name_edit)

        # 示例：添加学分输入框
        credits_edit = QLineEdit(self)
        form_layout.addRow("学分:", credits_edit)

        # 示例：添加先修课程输入框
        prereqs_edit = QLineEdit(self)
        form_layout.addRow("先修课程 (以逗号分隔):", prereqs_edit)

        # 示例：添加确认按钮
        confirm_button = QPushButton("确认", self)
        confirm_button.clicked.connect(self.accept)
        form_layout.addWidget(confirm_button)

        self.setLayout(form_layout)


# 新增的部分 - 用于修改最大学分限制的对话框
class ModifyMaxCreditsDialog(QDialog):
    def __init__(self, parent=None):
        super(ModifyMaxCreditsDialog, self).__init__(parent)
        self.setWindowTitle("修改最大学分限制")
        self.init_ui()

    def init_ui(self):
        # 在这里添加用于修改最大学分限制的界面元素
        form_layout = QFormLayout(self)

        # 示例：添加最大学分限制输入框
        max_credits_edit = QLineEdit(self)
        form_layout.addRow("最大学分限制:", max_credits_edit)

        # 示例：添加确认按钮
        confirm_button = QPushButton("确认", self)
        confirm_button.clicked.connect(self.accept)
        form_layout.addWidget(confirm_button)

        self.setLayout(form_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeachingPlanGenerator()
    window.show()
    sys.exit(app.exec_())
