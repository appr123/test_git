import heapq
import copy

class Node:
    def __init__(self, state, g=0, parent=None):
        self.state = state  # 一维列表表示4×4状态
        self.g = g          # 从初始到当前的步数
        self.parent = parent  # 父节点（用于回溯路径）
        self.h = self.calculate_heuristic()  # 启发值（曼哈顿距离和）
        # self.h=self.qifa_value1()
        self.f = self.g + self.h  # A*评估值

    def calculate_heuristic(self):
        """计算所有数码的曼哈顿距离之和"""
        heuristic = 0
        goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        for i in range(16):
            if self.state[i] != 0 and self.state[i] != goal[i]:
                # 当前位置(i//4, i%4)，目标位置(ti//4, ti%4)
                ti = goal.index(self.state[i])
                curr_x, curr_y = i // 4, i % 4
                target_x, target_y = ti // 4, ti % 4
                heuristic += abs(curr_x - target_x) + abs(curr_y - target_y)
        return heuristic

    def qifa_value1(self):#使用不在位的个数作为启发函数
        numb=0
        usal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        for k in range(16):
            if self.state[k] != 0 and self.state[k] != usal[k]:
                numb+=1
        return numb



    def __lt__(self, other):
        """优先队列排序依据：f值小的优先"""
        return self.f < other.f

    def get_blank_pos(self):
        """获取空格（0）的索引"""
        return self.state.index(0)

    def generate_children(self):
        """生成所有可能的子节点（空格上下左右移动）"""
        children = []
        blank_pos = self.get_blank_pos()
        blank_x, blank_y = blank_pos // 4, blank_pos % 4
        # 四个移动方向：上、下、左、右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = blank_x + dx, blank_y + dy
            if 0 <= new_x < 4 and 0 <= new_y < 4:  # 确保不越界
                new_blank_pos = new_x * 4 + new_y
                new_state = copy.deepcopy(self.state)
                # 交换空格与相邻数码
                new_state[blank_pos], new_state[new_blank_pos] = new_state[new_blank_pos], new_state[blank_pos]
                child = Node(new_state, self.g + 1, self)  # 子节点步数+1
                children.append(child)
        return children


def solve_15_puzzle(initial_state):
    """用A*算法求解十五数码问题"""
    initial_node = Node(initial_state)
    open_list = []          # 优先队列：存储待扩展节点
    heapq.heappush(open_list, initial_node)
    closed_set = set()      # 集合：存储已访问的状态
    closed_set.add(tuple(initial_state))

    search_count = 0        # 扩展节点计数
    max_open_size = 0       # Open表最大规模（用于分析）

    while open_list:
        # print(len(open_list))
        max_open_size = max(max_open_size, len(open_list))
        current_node = heapq.heappop(open_list)  # 取出f最小的节点
        search_count += 1

        # 检查是否达到目标状态
        if current_node.state == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]:
            # 回溯路径（从目标节点到初始节点）
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            path.reverse()  # 反转得到从初始到目标的路径
            print(f"搜索成功！共扩展{search_count}个节点，Open表最大规模{max_open_size}")
            return path

        # 生成子节点并加入Open表
        for child in current_node.generate_children():
            child_state = tuple(child.state)
            if child_state not in closed_set:
                closed_set.add(child_state)
                heapq.heappush(open_list, child)

    return None  # 无解（实际十五数码有解性由逆序数奇偶性决定，此处假设输入有解）



# 题目中的初始状态（空格在第二行第三列，对应索引6）
# initial_state = [11,9,4,15,1,3,0,12,7,5,8,6,13,2,10,14]
# initial_state=[1,2,3,4,5,6,7,8,9,10,12,15,13,14,11,0]

initial_state=[1,2,3,4,5,6,7,8,9,10,14,15,13,11,12,0]
path = solve_15_puzzle(initial_state)
if path:
    print("解决方案步骤（共{}步）：".format(len(path)-1))
    for i, state in enumerate(path):
        print(f"步骤 {i}:")
        for row in range(4):
            print(state[row*4 : row*4+4])  # 按行打印4×4网格
        print()
else:
    print("该初始状态无解！")





