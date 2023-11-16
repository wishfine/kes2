# utils.py
from collections import defaultdict
from course import Course
import re
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
