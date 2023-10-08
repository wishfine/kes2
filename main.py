from collections import defaultdict
from heapq import heappush, heappop
import re


class Course:
    def __init__(self, course_id, credits, prereqs):
        self.course_id = course_id
        self.credits = credits
        self.prereqs = prereqs


def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            semester_count, max_credits_per_semester = map(int, re.findall(r'\d+', file.readline()))
            course_info = {}
            for line in file:
                items = re.split(r'\s+', line.strip())
                course_id = items[0]
                credits = float(items[1])
                prereq = items[2].split(',') if items[2] != '-' else []
                course_info[course_id] = Course(course_id, credits, prereq)
            return semester_count, max_credits_per_semester, course_info
    except FileNotFoundError:
        print("找不到输入文件。")
        exit(1)
    except ValueError:
        print("输入格式错误。请检查输入文件。")
        exit(1)

def build_course_graph(course_info):
    course_graph = defaultdict(list)
    for course_id, course in course_info.items():
        for prereq_id in course.prereqs:
            course_graph[prereq_id].append(course_id)
    return course_graph


def topological_sort(course_graph):
    in_degree = defaultdict(int)
    for node in course_graph:
        for neighbor in course_graph[node]:
            in_degree[neighbor] += 1

    heap = []
    for node in course_graph:
        if in_degree[node] == 0:
            heappush(heap, node)

    topological_order = []
    while heap:
        node = heappop(heap)
        topological_order.append(node)
        for neighbor in course_graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heappush(heap, neighbor)

    return topological_order


def generate_teaching_plan(topological_order, max_credits_per_semester):
    teaching_plan = defaultdict(list)
    semester_credits = 0
    semester_number = 1

    for course_id in topological_order:
        course = course_info[course_id]
        if semester_credits + course.credits <= max_credits_per_semester:
            teaching_plan[semester_number].append(course_id)
            semester_credits += course.credits
        else:
            semester_number += 1
            teaching_plan[semester_number].append(course_id)
            semester_credits = course.credits

    return teaching_plan


def output_teaching_plan(teaching_plan, output_filename):
    with open(output_filename, 'w') as file:
        for semester_number, courses in teaching_plan.items():
            file.write(f"Semester {semester_number}:\n")
            for course_id in courses:
                file.write(f"{course_id}\n")


if __name__ == "__main__":
    # 读取输入文件
    filename = "input.txt"
    semester_count, max_credits_per_semester, course_info = read_input_file(filename)

    # 构建课程图
    course_graph = build_course_graph(course_info)

    # 拓扑排序
    topological_order = topological_sort(course_graph)

    # 生成教学计划
    teaching_plan = generate_teaching_plan(topological_order, max_credits_per_semester)

    # 输出教学计划
    output_filename = "teaching_plan.txt"
    output_teaching_plan(teaching_plan, output_filename)
