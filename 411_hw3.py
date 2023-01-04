''' CS 411 Homework 3: 15 Puzzle using BFS
    Name: Roselle Mata
'''
import math
import time
import os, psutil

'''
this function returns a list
the element in that list can be l,r,u,d 
refers to the movement of tiles
left, right, up,down
'''

def movements(cur):
    pair = []
    udlr_list = []
    
    for x in range(0, len(cur)):
      locate = eval(cur[x])
      y = 0
      
      while 0 not in locate[y]: 
        y += 1
        
      z = locate[y].index(0);   
      pair.append((y,z))

    for x in range(0, len(pair)-1):
      up = 0
      down = 0
      left = 0
      right = 0
          
      if pair[x][0] == pair[x+1][0]:
        if pair[x][1] > pair[x+1][1]:
          left = 1
        else:
          right = 1
          
      if (left == 1):
          udlr_list.append('l')
      if (right == 1):
          udlr_list.append('r')
          
      elif pair[x][1] == pair[x+1][1]:
        if pair[x][0] < pair[x+1][0]:
          down = 1
        else:
          up = 1

      if (down == 1):
          udlr_list.append('d')
      if (up == 1):
          udlr_list.append('u')


    return udlr_list

'''
this function
returns the
list of moves
'''
def moves(cur): 
    x = 0
    find = eval(cur)  
    
    while 0 not in find[x]: 
        x = x + 1
        
    up = 0
    down = 3
    left = 0
    right = 3
    udlr_list = []
    y = find[x].index(0);  

    if x > up:      
        e = find[x][y]
        up = find[x-1][y]
        e, up  = up, e
        move = str(find)
        udlr_list.append(move)
        e, up = up, e
    
    if y < right:        
        find[x][y], find[x][y+1] = find[x][y+1], find[x][y]
        move = str(find)
        udlr_list.append(move)
        find[x][y], find[x][y+1] = find[x][y+1], find[x][y]
      
    if x < down:                  
        find[x][y], find[x+1][y] = find[x+1][y], find[x][y]   
        move = str(find)
        udlr_list.append(move)
        find[x][y], find[x+1][y] = find[x+1][y], find[x][y]   

    if y > left:                   
        find[x][y], find[x][y-1] = find[x][y-1], find[x][y]   
        move = str(find)
        udlr_list.append(move)
        find[x][y], find[x][y-1] = find[x][y-1], find[x][y]   

    return udlr_list

'''
this is the 
bfs algorithm, 
takes input board and goal board
returns the shortest path when goal is reached
'''

def bfs_alg(cur_board, goal_board): 
    num_nodes = 0 
    front = [[cur_board]] 
    k = len(front)
    expanded = []
    
    while front: 
        i = 0
        for j in range(1, k):    
            if len(front[j]) < len(front[i]):
                i = j
                
        cur_path = front[i]         
        front = front[:i] + front[i+1:]
        end = cur_path[-1]
        
        if end in expanded:
            continue
          
        for each in moves(end):
            if each in expanded:
                continue
            front.append(cur_path + [each])
            
        expanded.append(cur_path[-1])
        num_nodes = num_nodes + 1
  
        if end == goal_board: 
            print ("Number of nodes expanded: ", num_nodes)
            return cur_path

# main
def main():
    start= time.time()
    board_given = str([[1, 0, 2,4],
                  [5,7,3,8], 
                  [9,6,11,12],
                  [13,10,14,15]])
    
    goal_board = str([[1, 2, 3, 4], 
                      [5, 6, 7, 8], 
                      [9, 10, 11, 12], 
                      [13, 14, 15, 0]])
                  
    result_board =  bfs_alg(board_given, goal_board)
    print("Time:" ,round((time.time() - start), 3), "seconds")
    print("Moves to reach the solution:", movements(result_board))
    process = psutil.Process(os.getpid())
    print("Memory usage: ", process.memory_info().rss)

if __name__ == '__main__': main()