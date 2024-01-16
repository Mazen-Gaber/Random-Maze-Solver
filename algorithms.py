import numpy as np
from mazeN_class import *

actions = ['U', 'D', 'L', 'R'] # UP , DOWN , LEFT , RIGHT

def is_valid_move(x, y, n, maze):
    if 0 <= x < n and 0 <= y < n and maze[x][y] != 0:
        return True
    return False

def value_iteration(maze, gamma=0.9, epsilon=1e-6):
    rows = cols = len(maze[0])
    
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny, rows):
                neighbors.append((nx, ny))
        return neighbors
    
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
    V = np.zeros((rows, cols))
    print("Iteration 0 :")
    k = 0
    for i in range(rows):
        print(V[i])
    
    while True:
        delta = 0
        k = k + 1
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] != 0:  # Ignore walls
                    max_q_value = float('-inf')
                    for action, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                        nx, ny = i + dx, j + dy
                        if is_valid_move(nx, ny, rows, maze):
                            p = 1  # Assuming deterministic transitions
                            if maze[i][j] == 3:
                                reward = 100    
                            else:
                                reward = -1
                            q_value = p * (reward + gamma * V[nx][ny])
                            max_q_value = max(max_q_value, q_value)

                    delta = max(delta, abs(max_q_value - V[i][j]))
                    V[i][j] = max_q_value
                    
        print("\n \n \n")
        print(f"Iteration {k} :")
        for i in range(rows):
            print(V[i])

        if delta < epsilon:
            break
    print("**********************")
    print("Total iterations: ", k)
    print("**********************")
    policy = np.zeros((rows, cols), dtype=str)
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] != 0:  # Ignore walls
                if maze[i][j] == 3:
                    policy[i][j] = 'S' # S -> stop
                    continue
                max_action = -1
                max_q_value = float('-inf')
                for action, (dx, dy) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                    nx, ny = i + dx, j + dy
                    if is_valid_move(nx, ny, rows, maze):
                        p = 1  
                        if maze[i][j] == 3:
                            reward = 10
                        else:
                            reward = -1
                        q_value = p * (reward + gamma * V[nx][ny])
                        if q_value > max_q_value:
                            max_q_value = q_value
                            max_action = action
                policy[i][j] = actions[max_action]
            elif maze[i][j] == 0:
                policy[i][j] = 'X '
    
    return V, policy

