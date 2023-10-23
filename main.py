import re
from collections import defaultdict

class Course:
    def __init__(self, course_name, credits, prereqs):
        self.course_name = course_name  # 中文课程名
        self.credits = credits  # 学分
        self.prereqs = prereqs  # 先修课程

def read_input_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            semester_count, max_credits_per_semester = map(int, re.findall(r'\d+', file.readline()))
            course_graph = defaultdict(list)
            course_info = {}

            for line in file:
                items = line.strip().split('\t')  # 使用制表符分隔
                course_name = items[0]  # 中文课程名
                credits = float(items[1])  # 学分
                prereq = [] if items[2] == '-' else items[2].split('，')  # 先修课程，使用中文逗号

                course = Course(course_name, credits, prereq)
                course_info[course_name] = course

                for prereq_name in prereq:
                    course_graph[prereq_name].append(course_name)

            return semester_count, max_credits_per_semester, course_info, course_graph
    except FileNotFoundError:
        print("找不到输入文件。")
        exit(1)
    except ValueError:
        print("输入格式错误。请检查输入文件。")
        exit(1)

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

        if semester_credits[semester_number] + course.credits > max_credits_per_semester:
            semester_number += 1
            semester_credits[semester_number] = 0

        teaching_plan[semester_number].append(course_name)
        semester_credits[semester_number] += course.credits
        course_semesters[course_name] = semester_number

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

if __name__ == "__main__":
    filename = "input2.txt"
    semester_count, max_credits_per_semester, course_info, course_graph = read_input_file(filename)

    topological_order = topological_sort(course_graph)

    teaching_plan, semester_credits, course_semesters = generate_teaching_plan(topological_order,
                                                                               max_credits_per_semester, semester_count,
                                                                               course_info)

    output_filename = "teaching_plan2.txt"
    output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename)
