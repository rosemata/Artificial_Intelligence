import time
import psutil
import os
import math


'''
initialize board
initialize swap of
up, left, down, right
'''
class board:
    def __init__(self, input_list):
        length_list = len(input_list)                   
        self.board_size = int(math.sqrt(length_list))   
        self.list = input_list                         
    
    def get_board(self):
        return self.list

    def move(self, move):
        cur_board = self.list[:]
        idx = cur_board.index('0')

        # up
        if move == 'U' and idx-4 >= 0:
            cur_board[idx-4], cur_board[idx] = cur_board[idx], cur_board[idx-4]
                
        # move to down
        if move == 'D' and idx+4 <= 15:
            cur_board[idx+4], cur_board[idx] = cur_board[idx], cur_board[idx+4]
        
        # move to left
        if move == 'L' and idx-1 >= 0:
            cur_board[idx-1], cur_board[idx] = cur_board[idx], cur_board[idx-1]

        
        # move to right
        if move == 'R' and idx+1 <= 15:
            cur_board[idx+1], cur_board[idx] = cur_board[idx], cur_board[idx+1]

        return board(cur_board)  
        

'''
Node class
'''
class Node:
    def __init__(self, state, parent, my_move, my_path, my_method):
        self.state = state
        self.parent = parent
        self.my_move = my_move
        self.my_path = my_path
        self.my_method = my_method
    
    def get_state(self):
        return self.state.list
    def get_state_str(self):
        x = ""
        for i in self.state.list:
            x = x + i
        return x
    def get_path(self):
        return self.my_path
    def get_method(self):
        return self.my_method
    def __lt__(self, other):
        return self.get_method() + self.get_path() < other.get_method() + other.get_path()
    
'''
Get the nodes from
up, down, left, right
using Misplaced Tiles
'''

def misplaced_function(i):
    moves = []
    moves.append(Node(i.state.move('U'), i, 'U', 1 + i.get_path(), misplaced_tiles_function(i.state.move('U'))))
    moves.append(Node(i.state.move('D'), i, 'D', 1  + i.get_path(), + misplaced_tiles_function(i.state.move('D'))))
    moves.append(Node(i.state.move('L'), i, 'L', 1 + i.get_path(), misplaced_tiles_function(i.state.move('L'))))
    moves.append(Node(i.state.move('R'), i, 'R', 1 + i.get_path(), misplaced_tiles_function(i.state.move('R'))))
    
    return moves

'''
Get the nodes from
up, down, left, right
using Manhattan Distance
'''
def manhattan_function(cur):
    moves = []
    moves.append(Node(cur.state.move('U'), cur, 'U', 1 + cur.get_path(), manhattan_distance_function(cur.state.move('U'))))
    moves.append(Node(cur.state.move('D'), cur, 'D', 1 + cur.get_path(), manhattan_distance_function(cur.state.move('D'))))
    moves.append(Node(cur.state.move('L'), cur, 'L', 1 + cur.get_path(), manhattan_distance_function(cur.state.move('L'))))
    moves.append(Node(cur.state.move('R'), cur, 'R', 1 + cur.get_path(), manhattan_distance_function(cur.state.move('R'))))
    return moves

'''
Get the path
'''
def get_path(cur):	
	move = []
    # when the node still have parent, save the action into list and get the parent node
	while(cur.parent):
		move.append(cur.my_move)
		cur = cur.parent
	return move

'''
Helper to Calculate Misplaced Tiles
'''

final_board = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
def misplaced_tiles_function (cur):
    
    board = cur.get_board()
    count = 0
    for i in range(16):
        if board[i] == final_board[i]:
            continue
        else:
            count = count + 1
    return count
        
'''
Helper to Calculate Manhattan Distance
'''
def manhattan_distance_function(cur):
    board = cur.get_board()
    count = 0
    for i in range(16):
        if board[i] == '0':
            continue
        else:
            if board[i] == final_board[i]:
                continue
            else:
                count = int(abs(final_board.index(board[i]) - board.index(board[i])) / 4 + abs(final_board.index(board[i]) - board.index(board[i])) % 4) + count
    return count

'''
Iterative Deepening a-star (IDA*) search
'''
def ida_star(cur, heuristic):

    if heuristic == 1:
        bound = misplaced_tiles_function(cur.state)
    elif heuristic == 2: 
        bound = manhattan_distance_function(cur.state)
    
    path = [cur]
    num_expand = 0
   
    # while solution not reach
    while 1:
        result, final_path, num_expand = search(path, 0, bound, heuristic, num_expand)
        # if start_puzzle == goal_puzzle
        if result == -1:
            return final_path, num_expand
        bound = result

'''
Search helper for ida_star
'''
def search(path, cur_total, bound, method, count):

    '''
    Check if goal reach helper
    '''
    def goal_reach(board):
        if board == final_board:
            return True
        else:
            return False

    min = 1000
    cur = path[-1]

    # Misplaced Tiles
    if method == 1:
        total = cur_total + misplaced_tiles_function(cur.state)
        if total > bound:
            return total, None, count
        # check if we reach goal
        if goal_reach(cur.state.get_board()):
            return -1, get_path(cur), count
        # List of moves left, right, up, down using misplaced tiles
        list_moves = misplaced_function(cur) 
        for move_to in list_moves:
            count = count + 1
            if move_to not in path:
                path.append(move_to)
                t, final_path, count = search(path, cur_total + 1, bound, method, count)
                if t == -1:
                    return -1, final_path, count
                if t < min:
                    min = t
                path.pop()

    # Manhattan Distance
    if method == 2:
        total = cur_total + manhattan_distance_function(cur.state)
        if total > bound:
            return total, None, count
        # check if we reach goal
        if goal_reach(cur.state.get_board()):
            return -1,  get_path(cur), count 
        # List of moves left, right, up, down using manhattan distance
        list_moves = manhattan_function(cur)
        for move_to in list_moves: 
            count = count + 1
            if move_to not in path:
                path.append(move_to)
                t, final_path, count = search(path, cur_total + 1, bound, method, count)
                if t == -1:
                    return -1, final_path, count
                if t < min:
                    min = t
                path.pop()
    
    return min, None, count

def main():
    # start memory, time count
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024
    start_time = time.time()

    # ask for input
    input_number = input("Input: ")
    method_use = input("1 for Misplaced Tiles / 2 for Manhattan Distance: ")

    # initialize board
    input_number_list = input_number.split()
    start_board = board(input_number_list)
    init_board = Node(start_board, None, None, 0, 0)    

    misplaced_tiles = 1
    manhattan_distance = 2

    # choose which method
    method = misplaced_tiles
    if method_use == 1:
        method = misplaced_tiles
    if method_use == 2:
        method = manhattan_distance

    # call ida* heuristic
    ida_star_heuristic = ida_star(init_board, method)
    total_moves = ''
    for i in ida_star_heuristic[0]:
        total_moves = total_moves + i

    # print moves, nodes count, time, memory
    print("Moves: %s" % total_moves)
    print ("Number of Nodes expanded: %d" % ida_star_heuristic[1])
    print("Time Taken: %s " % (time.time() - start_time))
    print("Memory Used: %d kb" % ((process.memory_info().rss / 1024) - start_memory))
    
if __name__ == "__main__":
    main()

# 1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15