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

def generate_teaching_plan(topological_order, max_credits_per_semester, max_semesters, course_info):
    teaching_plan = defaultdict(list)
    semester_credits = defaultdict(float)
    current_semester = 1
    course_semesters = {}  # 定义课程的学期

    for course_id in topological_order:
        course = course_info[course_id]
        prereq_semesters = [course_semesters.get(prereq_id, 0) for prereq_id in course.prerequisites]

        # 更新学期号
        if prereq_semesters:
            current_semester = max(prereq_semesters) + 1

        # 检查学期数限制
        if current_semester > max_semesters:
            break

        # 检查学分限制
        if semester_credits[current_semester] + course.credits > max_credits_per_semester:
            current_semester += 1

        # 更新教学计划和学分
        if current_semester <= max_semesters:
            teaching_plan[current_semester].append((course_id, course.credits))
            semester_credits[current_semester] += course.credits
            course_semesters[course_id] = current_semester

    return teaching_plan, semester_credits, course_semesters


def output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename):
    with open(output_filename, 'w') as file:
        for semester_number, courses in teaching_plan.items():
            file.write(f"学期 {semester_number}:\n")
            file.write(f"所修学分: {semester_credits[semester_number]:.2f}\n")
            file.write("课程列表:\n")
            for course_id in courses:
                course = course_info[course_id]
                file.write(f"{course_id} - {course.credits} 学分\n")

if __name__ == "__main__":
    filename = "input.txt"
    semester_count, max_credits_per_semester, course_info, course_graph = read_input_file(filename)

    topological_order = topological_sort(course_graph)

    # 初始化学期号和学分
    semester_number = 1
    semester_credits = defaultdict(float)
    course_semesters = {}

    # 用于存储每个学期的课程
    teaching_plan = defaultdict(list)

    for course_id in topological_order:
        course = course_info[course_id]
        prereq_semesters = [course_semesters.get(prereq_id, 0) for prereq_id in course.prereqs]

        # 更新学期号
        if prereq_semesters and max(prereq_semesters) == semester_number:
            semester_number += 1
            semester_credits[semester_number] = 0

        # 检查学分限制
        if semester_credits[semester_number] + course.credits > max_credits_per_semester:
            semester_number += 1
            semester_credits[semester_number] = 0

        # 更新教学计划和学分
        teaching_plan[semester_number].append(course_id)
        semester_credits[semester_number] += course.credits
        course_semesters[course_id] = semester_number

    output_filename = "teaching_plan.txt"
    output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename)
