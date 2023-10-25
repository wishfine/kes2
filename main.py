import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
from collections import defaultdict

class Course:
    def __init__(self, course_name, credits, prereqs):
        self.course_name = course_name
        self.credits = credits
        self.prereqs = prereqs

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
        messagebox.showerror("Error", "找不到输入文件。")
        return None
    except ValueError:
        messagebox.showerror("Error", "输入格式错误。请检查输入文件。")
        return None

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

        teaching_plan[semester_number].append(course_name)
        semester_credits[semester_number] += course.credits
        course_semesters[course_name] = semester_number

    return teaching_plan, semester_credits, course_semesters

def generate_balanced_teaching_plan(topological_order, max_credits_per_semester, max_semesters, course_info):
    semester_number = 1
    course_queue = list(topological_order)
    semester_credits = defaultdict(float)
    course_semesters = {}
    teaching_plan = defaultdict(list)

    while course_queue:
        current_course = course_queue.pop(0)
        course = course_info[current_course]
        prereq_semesters = [course_semesters.get(prereq_name, 0) for prereq_name in course.prereqs]

        if prereq_semesters and max(prereq_semesters) == semester_number:
            semester_number += 1
            semester_credits[semester_number] = 0

        while semester_credits[semester_number] + course.credits > max_credits_per_semester:
            semester_number += 1
            if semester_number > max_semesters:
                raise Exception("无法满足学分限制和课程先修条件。")

        teaching_plan[semester_number].append(current_course)
        semester_credits[semester_number] += course.credits
        course_semesters[current_course] = semester_number

    return teaching_plan, semester_credits, course_semesters

def output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for semester_number, courses in teaching_plan.items():
            file.write(f"学期 {semester_number}:\n")
            file.write(f"所修学分: {semester_credits[semester_number]:.2f}\n")
            file.write("课程列表:\n")
            for course_name in courses:
                course = course_info[course_name]
                file.write(f"{course.course_name} - {course.credits} 学分\n")

def browse_input_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    input_filename.set(filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")])
    output_filename.set(filename)

def generate_plan():
    input_file = input_filename.get()
    output_file = output_filename.get()
    plan_type = generate_mode.get()
    if not input_file or not output_file:
        messagebox.showerror("Error", "请输入输入和输出文件名。")
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
                teaching_plan, semester_credits, course_semesters = generate_balanced_teaching_plan(topological_order,
                                                                                                    max_credits_per_semester,
                                                                                                    semester_count,
                                                                                                    course_info)

            output_teaching_plan(teaching_plan, semester_credits, course_info, output_file)
            messagebox.showinfo("Success", "教学计划已生成成功！")
    except Exception as e:
        messagebox.showerror("Error", str(e))

window = tk.Tk()
window.title("课程教学计划生成器")
window.geometry("400x250")

tk.Label(window, text="输入文件：").grid(row=0, column=0, padx=10, pady=10)
input_filename = tk.StringVar()
input_entry = tk.Entry(window, textvariable=input_filename, width=30)
input_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Label(window, text="输出文件：").grid(row=1, column=0, padx=10, pady=10)
output_filename = tk.StringVar()
output_entry = tk.Entry(window, textvariable=output_filename, width=30)
output_entry.grid(row=1, column=1, padx=10, pady=10)

browse_input_button = tk.Button(window, text="浏览", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=10)
browse_output_button = tk.Button(window, text="浏览", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=10, pady=10)

generate_mode_label = tk.Label(window, text="生成方式:")
generate_mode_label.grid(row=2, column=0, padx=10, pady=10)

generate_mode = tk.StringVar()
generate_mode.set("尽快修完所有课程")

generate_mode_menu = tk.OptionMenu(window, generate_mode, "尽快修完所有课程", "每学期学习负担尽可能相同")
generate_mode_menu.grid(row=2, column=1, padx=10, pady=10)

generate_button = tk.Button(window, text="生成教学计划", command=generate_plan, width=30, height=2)
generate_button.grid(row=3, column=0, columnspan=3, pady=10)

window.mainloop()
