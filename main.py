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
            #re.findall(r'\d+', file.readline()):
            # 这一部分使用正则表达式 (re 模块) 在读取的行中查找所有的数字。正则表达式 r'\d+' 匹配一个或多个数字。
            #map()函数将正则表达式找到的数字字符串转换为整数
            course_graph = defaultdict(list)  # 课程图
            course_info = {}  # 课程信息

            # 逐行读取课程信息
            for line in file:
                items = re.split(r'\s+', line.strip())
                #strip() 函数用于去除字符串两端的空格和换行符
                #\s + 表示匹配一个或多个空白字符，包括空格、制表符、换行等
                course_id = items[0]  # 课程ID
                credits = float(items[1])  # 学分
                prereq = items[2].split(',') if items[2] != '-' else []  # 先修课程
                #如果第三个元素不是 '-'，则对该元素使用 split(',') 方法进行拆分。
                # split(',') 方法将字符串按逗号 , 进行拆分，返回一个由拆分后的子字符串组成的列表。

                # 构建课程对象
                course = Course(course_id, credits, prereq)
                course_info[course_id] = course
                #course_info 是一个字典，用于存储课程信息，以课程ID (course_id) 作为键，将课程对象 (course) 作为值存储起来。

                # 构建课程图
                for prereq_id in prereq:
                    course_graph[prereq_id].append(course_id)
                #当前课程ID (course_id) 添加到先修课程ID (prereq_id) 对应的列表中，表示当前课程是该先修课程的后续课程
            return semester_count, max_credits_per_semester, course_info, course_graph
    except FileNotFoundError:
        print("找不到输入文件。")
        exit(1)
    except ValueError:
        print("输入格式错误。请检查输入文件。")
        exit(1)

def topological_sort(course_graph):
    #课程图中每个节点（课程）的入度（in-degree）字典
    in_degree = defaultdict(int)
    #构建课程图中课程节点的入度信息
    for node in course_graph:
        for neighbor in course_graph[node]: #当前课程后续课程遍历
            in_degree[neighbor] += 1  #当前后续课程的入度加1


    current_stack = []
    backup_stack = []

    for node in course_graph:
        if in_degree[node] == 0:
            current_stack.append(node)

    topological_order = []  #存储拓扑排序后的课程节点顺序

    while current_stack or backup_stack: #直到 current_stack 和 backup_stack 都为空结束
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
    # 初始化学期号和学分
    semester_number = 1
    semester_credits = defaultdict(float)
    course_semesters = {}

    # 用于存储每个学期的课程
    teaching_plan = defaultdict(list)

    for course_id in topological_order:
        course = course_info[course_id]
        #创建一个列表 prereq_semesters，存储当前课程的先修课程所在的学期
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
    return teaching_plan, semester_credits, course_semesters



def output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename):
    # 将学期号、已修学分、以及每个学期的课程列表输出到文件中
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

    teaching_plan, semester_credits, course_semesters = generate_teaching_plan(topological_order,
                                                                               max_credits_per_semester, semester_count,
                                                                               course_info)

    output_filename = "teaching_plan.txt"
    output_teaching_plan(teaching_plan, semester_credits, course_info, output_filename)
