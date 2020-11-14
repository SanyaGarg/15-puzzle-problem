#!/usr/bin/env python3
import time
import numpy as np
import copy
from heapq import *

                     
def Manhattan(row,col,position):
    goalx = position[0]
    goaly = position[1]

    i = abs(row-goalx)
    j = abs(col - goaly)

    return (i+j)

def heuristic(State,):
    pos = {'0':[0,0],'1':[0,1],'2':[0,2],'3':[0,3],'4':[1,0],'5':[1,1],'6':[1,2],'7':[1,3],'8':[2,0],'9':[2,1],'A':[2,2],'B':[2,3],'C':[3,0],'D':[3,1],'E':[3,2],'F':[3,3]}
    h =0
    
    #print(State[10])
    #manhattan
    for i in range(0,4):
        for j in range(0,4):
            if State[4*i+j]!='0':
                   h+= Manhattan(i,j,pos[State[4*i+j]])
    #print(h)

    goal_row = "0123456789ABCDEF"
    goal_col = "048C159D26AE37BF"

    for m in range(4):
        cur_col = goal_col[4*m:4*m+4]
        new_s=[]
        for row in range(4):
            i=row*4 + m
            if State[i] in cur_col:
                new_s.append(State[i])
 
        n = len(new_s)
        for j in range(n):
            for k in range(j+1,n):
                a= ord(new_s[k])-ord("0")
                b = ord(new_s[j])-ord("0")
                if(a>0 and a < b):
                    h+=2

    for k in range(16):
        if(k%4==0):
            row = goal_row[k:k+4]
            new_state = []

        if(State[k] in row):
            new_state.append(State[k])

        n = len(new_state)  
        for j in range(n):
            for i in range(j+1,n):
                a= ord(new_state[i])-ord("0")
                b = ord(new_state[j])-ord("0")
                if(a>0 and a < b):
                    h+=2      
    return h
  
    
def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    hp = []    
    
    goal_row = "0123456789ABCDEF"
    
    depth = {}
    state = ""  

    for k in initialState:
        for l in k:
            state+= l

    depth[state]=0
    f = heuristic(state)+depth[state]

    direction = []
    heappush(hp,(f,state,direction))

    while True:

        curr_tuple = heappop(hp)
        f = curr_tuple[0]
        curr_node = curr_tuple[1]
        direction = copy.deepcopy(curr_tuple[2])
        #print(direction)
        if(curr_node==goal_row):
            minPath = direction
            break

        empty_tile = curr_node.index('0')
            #print(empty_tile-1)
        i_emp = (empty_tile)//4
        j_emp = (empty_tile)%4

        array_x = [-1,1,0,0]
        array_y = [0,0,-1,1]
        
        for i in range(4):

            new_i = i_emp+array_x[i]
            new_j = j_emp+array_y[i]

            if(new_i>=0 and new_i<4 and new_j>=0 and new_j<4):
                swap_state = ""

                for j in range(16):
                    x=j//4
                    y=j%4

                    if(x==i_emp and y ==j_emp):
                        swap_state+=curr_node[4*new_i+new_j]
                    elif(x==new_i and y ==new_j):
                        swap_state+=curr_node[4*i_emp+j_emp]
                    else:
                        swap_state+=curr_node[j]
            
                Cost = depth[curr_node] + 1
                if swap_state not in depth or Cost<depth[swap_state]:
                    depth[swap_state] = Cost
                    f = Cost + heuristic(swap_state)

                    action = copy.deepcopy(direction)
                    if(i==0):
                        action.append("DOWN")
                    elif(i==1):
                        action.append("UP") 
                    elif(i==2):
                        action.append("RIGHT")
                    elif(i==3):
                        action.append("LEFT")
                    
                    
                    heappush(hp,(f,swap_state,action))
                    nodesGenerated+=1
                    

    
    return minPath, nodesGenerated       

    #**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state1.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    #heuristic(initialState)
    goal =np.array(goalState)
    #print(type(goal[2][2]))
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
