import os
import time
import itertools
import psutil


class Node:
    def __init__(self, value):
        self.child1 = None
        self.child2 = None
        self.child3 = None
        self.child4 = None
        self.parent = None
        self.value = value

movesList = []
board_list = []
expanded_nodes = []

'''This function
creates tree
and insert nodes to the tree'''
class Tree:
    def createNode(self, value):
        return Node(value)

    def insert(self, node, data):
        # base case
        if node is None:
            return self.createNode(data)
        # if data is smaller than parent , insert it into left side
        if node.data == data:
            return node

        # left
        elif node.child1 == None:
            node.child1 = self.insert(node.lchild1eft, data)

        # right
        elif node.child2 == None:
            node.child2 = self.insert(node.child2, data)

        # any
        elif node.child3 == None:
            node.child3 = self.insert(node.child3, data)

        # any
        else:
            node.child4 = self.insert(node.child4, data)

        return node

'''
helper for
moves function
'''
def move_up(x,y, board):
    board[x][y], board[x - 1][y] = board[x - 1][y], board[x][y]
    board_list.append(str(board))
    board[x][y], board[x - 1][y] = board[x - 1][y], board[x][y]
    movesList.append('U')

def move_down(x,y,board):
    board[x][y], board[x + 1][y] = board[x + 1][y], board[x][y]
    board_list.append(str(board))
    board[x][y], board[x + 1][y] = board[x + 1][y], board[x][y]
    movesList.append('D')

def move_left(x,y,board):
    board[x][y], board[x][y - 1] = board[x][y - 1], board[x][y]
    board_list.append(str(board))
    movesList.append('L')
    board[x][y], board[x][y - 1] = board[x][y - 1], board[x][y]

def move_right(x,y,board):
    board[x][y], board[x][y + 1] = board[x][y + 1], board[x][y]
    board_list.append(str(board))
    board[x][y], board[x][y + 1] = board[x][y + 1], board[x][y]
    movesList.append('R')

''''
this function
moves
up, left, down, rihgt
and append those
moves to a moves list
and append the board
the boards list'''
def moves(input):
    cur_board = eval(input)
    x = 0
    while 0 not in cur_board[x]:
        x = x + 1
    y = cur_board[x].index(0)

    if x > 0:  # Shifting UP
        move_up(x,y,cur_board)

    if x < 3:  # Shifting DOWN
        move_down(x,y,cur_board)

    if y > 0:  # Shifting LEFT
        move_left(x,y,cur_board)

    if y < 3:  # Shifting RIGHT
        move_right(x,y,cur_board)

    return board_list

'''
This
Functions
Implements
Manhattan
Heuristic
'''

def manhattan_distance_heuristic(start_board, finalBoard):
    '''
    helper to calcualte
    distance between
    tiles
    
    '''
    def manhattan_distance(initialBoard):
        distance = 0
        board = eval(initialBoard)
        for i in range(0, 4):
            for j in range(0, 4):
                if board[i][j] == 0:
                    continue
                distance = distance + abs(i - board[i][j]/4) + abs(j - board[i][j]%4)
        return distance

    top = [[manhattan_distance(start_board), start_board]]
    while top:
        i=0
        for j in range(1, len(top)):
            if top[i][0] > top[j][0]:
                i=j
        path = top[i]
        top = top[:i] + top[i+1:]
        end_board = path[-1]
        if end_board == finalBoard:
            break
        for move in moves(end_board):
            newPath = [path[0] + manhattan_distance(move) - manhattan_distance(end_board)] + path[1:] + [move]
            expanded_nodes.append(end_board)


'''
This function
implements
Misplaced
Tiles
Heuristic
'''
def misplace_tiles_heuristic(start_board, final_board):

    """"
    helper to count
    number of misplace tiles
    """
    def num_misplaced_tiles(start_board):

        num_misplaced = 0
        num_match = 0
        for x in range(0, 4):
            for y in range(0, 4):
                if  eval(start_board)[x][y] == num_match:
                    num_match += 1
                elif  eval(start_board)[x][y] != num_match:
                    num_misplaced = num_misplaced + 1
                else:
                    num_match += 1
        return num_misplaced

    top = [[num_misplaced_tiles(start_board), start_board]]
    while top:
        x=0
        for j in range(1, len(top)):
            if top[x][0] > top[j][0]:
                i=j

        path = top[x]
        top = top[:x] + top[x+1:]
        end_board = path[-1]

        if end_board == final_board:
            break
        for move in moves(end_board):
            newPath = [path[0] + num_misplaced_tiles(move) - num_misplaced_tiles(end_board)] + path[1:] + [move]
            expanded_nodes.append(end_board)

def main():
    prompt = input("Enter number 0-15 numbers in random order: ")
    #check error
    starting_puzzle = prompt
    starting_puzzle = starting_puzzle.replace(" ", ",")
    starting_puzzle = [str(i) for i in starting_puzzle.split(',')]
    starting_puzzle = list(map(int, starting_puzzle))
    if len(starting_puzzle) != 16:
        print("Input incorrect. Try again...")
        main()

    # format the input helper
    def format(starting_input):
        new_board = []
        starting_input = starting_input.replace(" ", ",")
        revised_input = [str(k) for k in starting_input.split(',')]
        revised_input = list(map(int, revised_input))
        for i in range(0, len(revised_input), 4):
            new_board.append(revised_input[i:i + 4])
        return new_board

    choice = input('Enter 1 for Manhattan Distance or 2 for Number of Misplaced Tiles: ')
    start_board = str(format(prompt))
    final_board = str([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

    startTime = time.time()
    process = psutil.Process(os.getpid())
    initialMemory = process.memory_info().rss / 1024.0

    if choice == '1':
        print()
        print('Solution with choice 1 Manhattan Distance')
        manhattan_distance_heuristic(start_board, final_board)
    elif choice == '2':
        print()
        print('Solution with choice 2 Number of Misplaced Tiles')
        misplace_tiles_heuristic(start_board, final_board)
    else:
        print('Wrong Input')
        main()

    print('Moves Taken: ', end="")
    for i in range(len(movesList)):
        print(movesList[i], end="")
    print()

    total_memory = (process.memory_info().rss / 1024.0) - initialMemory
    total_time = time.time() - startTime
    print('Expanded Nodes: ' + str(len(expanded_nodes)))
    print('Time taken: ' + str(total_time))
    print('Total Memory used: ' + str(total_memory) + ' KB')
    return

if __name__=="__main__":main()

