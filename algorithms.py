import numpy as np
from mazeN_class import *

actions = ['U', 'D', 'L', 'R'] # UP , DOWN , LEFT , RIGHT

def is_valid_move(x, y, n, maze):
    if 0 <= x < n and 0 <= y < n and maze[x][y] != 0:
        return True
    return False

def get_valid_actions(maze, state):
    actions = []
    row, col = state
    if row > 0 and maze[row-1][col] != 0:
        actions.append('U')
    if row < len(maze)-1 and maze[row+1][col] != 0:
        actions.append('D')
    if col > 0 and maze[row][col-1] != 0:
        actions.append('L')
    if col < len(maze[0])-1 and maze[row][col+1] != 0:
        actions.append('R')
    return actions

def value_iteration(maze, gamma=0.7, epsilon=0.00001, max_k = 600):
    rows = cols = len(maze[0])
    
    start_cell = None
    goal_cell = None
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 2:
                start_cell = (i, j)
            elif maze[i][j] == 3:
                goal_cell = (i, j)
    
    
    if start_cell is None or goal_cell is None:
        raise ValueError("Can't find both start and goal cells!")
    
    reward = np.zeros((rows, cols))
    # Intializing v0(s)
    V = np.zeros((rows, cols))
    print("Iteration 0 :")
    
    for i in range(rows):
        print(V[i])
    
    k = 1
    while True:
        delta = 0
        k = k + 1
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] != 0: 
                    max_v_iter = float('-inf')
                    for action, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                        nx, ny = i + dx, j + dy
                        if is_valid_move(nx, ny, rows, maze):
                            p = 1  
                            if maze[i][j] == 3:
                                reward = 10    
                            else:
                                reward = -1
                            v_iter = p * (reward + gamma * V[nx][ny])
                            max_v_iter = max(max_v_iter, v_iter)

                    delta = max(delta, abs(max_v_iter - V[i][j]))
                    V[i][j] = max_v_iter
                    
        print("\n \n \n")
        print(f"Iteration {k} :")
        print("Current Value function:")
        print("***********************")
        for i in range(rows):
            print(V[i])

        if delta < epsilon or k >= max_k:
            break
    print("**********************")
    print("Total iterations: ", k)
    print("**********************")
    policy = np.zeros((rows, cols), dtype=str)
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] != 0:  
                if maze[i][j] == 3:
                    policy[i][j] = 'S' # S -> stop
                    continue
                max_action = -1
                max_v_iter = float('-inf')
                for action, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                    nx, ny = i + dx, j + dy
                    if is_valid_move(nx, ny, rows, maze):
                        p = 1  
                        if maze[i][j] == 3:
                            reward = 10
                        else:
                            reward = -1
                        v_iter = p * (reward + gamma * V[nx][ny])
                        if v_iter > max_v_iter:
                            max_v_iter = v_iter
                            max_action = action
                policy[i][j] = actions[max_action]
            elif maze[i][j] == 0:
                policy[i][j] = 'X ' # X -> wall
    
    return V, policy

def policy_evaluation(maze, policy, gamma=0.7, epsilon=0.00001):
    V = np.zeros_like(maze, dtype=np.float32)
    while True:
        delta = 0.0

        for row in range(len(maze)):
            for col in range(len(maze[0])):
                reward = -1
                if maze[row][col] == 0:
                    continue
                if maze[row][col] == 3:
                    reward = 10
                old_value = V[row][col]
                action = policy[row][col]
                if action == 'U' and row > 0:
                    new_value = reward + gamma * V[row-1][col]
                elif action == 'D' and row < len(maze)-1:
                    new_value = reward + gamma * V[row+1][col]
                elif action == 'L' and col > 0:
                    new_value = reward + gamma * V[row][col-1]
                elif action == 'R' and col < len(maze[0])-1:
                    new_value = reward + gamma * V[row][col+1]
                else:
                    new_value = 0.0  # 0 for invalid actions
                V[row][col] = new_value
                delta = max(delta, abs(old_value - new_value))
        if delta < epsilon:
            break
    return V

def policy_improvement(maze, V, gamma=0.7):
    policy = np.empty_like(maze, dtype=object)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 3:
                policy[row][col] = 'S'
                continue
            if maze[row][col] == 0:
                policy[row][col] = 'X'
                continue
            best_action = None
            best_value = float('-inf')
            actions = get_valid_actions(maze, (row, col))
            for action in actions:
                if action == 'U' and row > 0:
                    value = gamma * V[row-1][col]
                elif action == 'D' and row < len(maze)-1:
                    value = gamma * V[row+1][col]
                elif action == 'L' and col > 0:
                    value = gamma * V[row][col-1]
                elif action == 'R' and col < len(maze[0])-1:
                    value = gamma * V[row][col+1]
                if value > best_value:
                    best_value = value
                    best_action = action
            policy[row][col] = best_action
    return policy

def policy_iteration(maze):
    policy = np.random.choice(actions, size=(len(maze), len(maze[0])))
    i = 0
    while True:
        V = policy_evaluation(maze, policy)
        print("\n \n \n")
        print(f"Iteration {i} :")
        print("Current Value function:")
        print("***********************")
        for j in range(len(maze[0])):
            print(V[j])
        i = i+1
        new_policy = policy_improvement(maze, V)
        print("Current policy:")
        print("***********************")
        for j in range(len(maze[0])):
            print(new_policy[j])
        if np.all(policy == new_policy): # Calculating the L1 norm distance 
            break
        policy = new_policy
    return policy, V, i