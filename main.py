import re
from collections import defaultdict

class Course:
    def __init__(self, course_id, credits, prereqs):
        self.course_id = course_id  # 课程ID
        self.credits = credits  # 学分
        self.prereqs = prereqs  # 先修课程

def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            # 从文件中读取学期数和每学期最大学分
            semester_count, max_credits_per_semester = map(int, re.findall(r'\d+', file.readline()))
            course_graph = defaultdict(list)  # 课程图
            course_info = {}  # 课程信息

            # 逐行读取课程信息
            for line in file:
                items = re.split(r'\s+', line.strip())
                course_id = items[0]  # 课程ID
                credits = float(items[1])  # 学分
                prereq = items[2].split(',') if items[2] != '-' else []  # 先修课程

                # 构建课程对象
                course = Course(course_id, credits, prereq)
                course_info[course_id] = course

                # 构建课程图
                for prereq_id in prereq:
                    course_graph[prereq_id].append(course_id)

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

def generate_teaching_plan(topological_order, max_credits_per_semester):
    teaching_plan = defaultdict(list)
    semester_credits = 0
    semester_number = 1
    course_semesters = defaultdict(int)

    for course_id in topological_order:
        course = course_info[course_id]
        prereq_semesters = [course_semesters[prereq_id] for prereq_id in course.prereqs]

        if prereq_semesters and max(prereq_semesters) == semester_number:
            semester_number += 1
            semester_credits = 0

        if semester_credits + course.credits > max_credits_per_semester:
            semester_number += 1
            semester_credits = 0

        teaching_plan[semester_number].append(course_id)
        semester_credits += course.credits
        course_semesters[course_id] = semester_number

    return teaching_plan

def output_teaching_plan(teaching_plan, output_filename):
    with open(output_filename, 'w') as file:
        for semester_number, courses in teaching_plan.items():
            file.write(f"学期 {semester_number}:\n")
            for course_id in courses:
                file.write(f"{course_id}\n")

if __name__ == "__main__":
    filename = "input.txt"
    # 读取输入文件并获取学期数、每学期最大学分、课程信息和课程图
    semester_count, max_credits_per_semester, course_info, course_graph = read_input_file(filename)

    # 拓扑排序
    topological_order = topological_sort(course_graph)

    # 生成教学计划
    teaching_plan = generate_teaching_plan(topological_order, max_credits_per_semester)

    # 输出教学计划
    output_filename = "teaching_plan.txt"
    output_teaching_plan(teaching_plan, output_filename)
