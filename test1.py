import random
import tkinter as tk
from copy import deepcopy
from colorama import Fore, Back, Style


DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'


bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'


first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL


def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)


class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))

    return listNode

def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

# Hàm kiểm tra số đảo chẵn (đảm bảo bài toán có thể giải quyết được)
def is_solvable(puzzle):
    flat_puzzle = [item for row in puzzle for item in row]
    inversions = 0
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] != 0 and flat_puzzle[j] != 0 and flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

# Hàm tạo ma trận ngẫu nhiên có thể giải được
def generate_random_puzzle():
    while True:
        puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Ma trận ban đầu
        flat_puzzle = [item for row in puzzle for item in row]
        random.shuffle(flat_puzzle)
        # Chia lại danh sách thành ma trận 3x3
        puzzle = [flat_puzzle[i:i+3] for i in range(0, len(flat_puzzle), 3)]
        if is_solvable(puzzle):  # Kiểm tra xem ma trận có thể giải được không
            return puzzle

# main function of node
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

# Tkinter GUI code
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver")
        
        # Tạo GUI
        self.start_button = tk.Button(root, text="Start Puzzle", command=self.solve_puzzle)
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset Puzzle", command=self.reset_puzzle)
        self.reset_button.pack(pady=10)

        self.back_button = tk.Button(root, text="Back", command=self.back_step, state=tk.DISABLED)
        self.back_button.pack(pady=10)

        self.forward_button = tk.Button(root, text="Forward", command=self.forward_step, state=tk.DISABLED)
        self.forward_button.pack(pady=10)

        self.steps_label = tk.Label(root, text="Total steps: 0")
        self.steps_label.pack(pady=10)
        
        self.puzzle_frame = tk.Frame(root)
        self.puzzle_frame.pack()

        self.directions_label = tk.Label(root, text="Directions will appear here.")
        self.directions_label.pack(pady=10)

        # Hiển thị ma trận ban đầu chưa giải
        self.puzzle = generate_random_puzzle()
        self.display_puzzle(self.puzzle)
        
        # Hiển thị bước hiện tại
        self.current_step_label = tk.Label(root, text="Current Step: 0")
        self.current_step_label.pack(pady=10)
        
    def solve_puzzle(self):
        # Giải bài toán khi bấm "Start"
        self.steps = main(self.puzzle)

        # Loại bỏ bước đầu tiên (vì đó là trạng thái ban đầu chưa giải)
        self.steps = self.steps[1:]

        # Cập nhật số bước (không tính bước ban đầu)
        self.steps_label.config(text=f"Total steps: {len(self.steps)}")

        # Hiển thị bước đầu tiên (bước di chuyển đầu tiên)
        self.step_index = 0
        self.display_step(self.step_index)

        # Cập nhật trạng thái của các nút điều khiển
        self.back_button.config(state=tk.NORMAL)
        self.forward_button.config(state=tk.NORMAL)
        
    def back_step(self):
        # Lùi lại một bước
        if self.step_index > 0:
            self.step_index -= 1
            self.display_step(self.step_index)

    def forward_step(self):
        # Tiến lên một bước
        if self.step_index < len(self.steps) - 1:
            self.step_index += 1
            self.display_step(self.step_index)

    def reset_puzzle(self):
        # Reset ma trận và hiển thị lại
        self.puzzle = generate_random_puzzle()
        self.display_puzzle(self.puzzle)

        # Cập nhật số bước và trạng thái
        self.steps_label.config(text="Total steps: 0")
        self.current_step_label.config(text="Current Step: 0")
        self.step_index = 0
        self.back_button.config(state=tk.DISABLED)
        self.forward_button.config(state=tk.DISABLED)

    def display_puzzle(self, puzzle):
        # Xóa các widget cũ trong frame
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()

        # Hiển thị ma trận hiện tại
        for row in puzzle:
            for num in row:
                label = tk.Label(self.puzzle_frame, text=str(num), width=4, height=2, relief="solid")
                label.grid(row=puzzle.index(row), column=row.index(num), padx=5, pady=5)

    def display_step(self, index):
        # Hiển thị bước hiện tại
        step = self.steps[index]
        self.display_puzzle(step['node'])
        self.directions_label.config(text=f"Move: {step['dir']}")
        self.current_step_label.config(text=f"Current Step: {index + 1}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = PuzzleGUI(root)
    root.mainloop()
