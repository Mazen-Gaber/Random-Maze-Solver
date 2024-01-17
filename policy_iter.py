import time
import numpy as np

def get_next_state(maze,N):
    """
    Given a maze compute the next state for each cell
    
    Args:
        maze: [N, N] shaped matrix representing the maze.
        N: Dimension of the maze
    
    Returns:
       [N*N, 4] representing the next state of each maze cell.
    """
    indx = np.zeros([N,N])    
    s=0
    for i in range(N):
        for j in range(N):
            indx[i][j]=s
            s+=1    
    next_state = np.zeros([N*N, 4])
    s=0
    for i in range(N):
        for j in range(N):
            if(i-1<0 or maze[i-1][j] == '#'):
                next_state[s][0] = s
            else:
                next_state[s][0] = indx[i-1][j]
                
            if(j+1>N-1 or maze[i][j+1] == '#'):
                next_state[s][1] = s
            else:
                next_state[s][1] = indx[i][j+1]
                
            if(i+1>N-1 or maze[i+1][j] == '#'):
                next_state[s][2] = s
            else:
                next_state[s][2] = indx[i+1][j]
                
            if(j-1<0 or maze[i][j-1] == '#'):
                next_state[s][3] = s
            else:
                next_state[s][3] = indx[i][j-1]
            
            if(maze[i][j] == '#' or ((i-1<0 or maze[i-1][j] == '#') and (j+1>N-1 or maze[i][j+1] == '#') and (i+1>N-1 or maze[i+1][j] == '#') and (j-1<0 or maze[i][j-1] == '#'))):
                next_state[s][0] = -1
                next_state[s][1] = -1
                next_state[s][2] = -1
                next_state[s][3] = -1
                
            if(maze[i][j] == 'G'):
                next_state[s][0] = s
                next_state[s][1] = s
                next_state[s][2] = s
                next_state[s][3] = s
            s+=1
    return next_state


def get_path_policy(p):
    finished = False
    path = []
    actions = []
    next_square = 0
    while finished == False:
        finished = True
        for i in range(4):
            if p[next_square][i] == 1:
                finished = False
                if i == 0:
                    next_square -= N
                    actions.append("up")
                elif i == 1:
                    next_square += 1 
                    actions.append("right")
                elif i == 2:
                    next_square += N 
                    actions.append("bottom")
                else:
                    next_square -= 1
                    actions.append("left")
                path.append(next_square)
    return (path,actions)

def is_deterministic(policy):
    """
    Given a policy the function checks wether it is detereministic policy or not
    
    Args:
        policy: matrix representing the policy.
            
    Returns:
       True if deterministic False otherwise
    """
    rows = policy.shape[0]
    cols = policy.shape[1]
    for x in range(0, rows):
        for y in range(0, cols):
            if abs(policy[x,y]-0.25)<0.0001:
                return False
    return True 
    
def policy_eval(policy, reward, next_state,V_old, discount_factor=1.0, theta=0.00001):
    """
    Evaluate a policy given an environment and a full description of the environment's dynamics.
    
    Args:
        policy: [S, A] shaped matrix representing the policy.
        env: OpenAI env. env.P represents the transition probabilities of the environment.
            env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
            env.nS is a number of states in the environment. 
            env.nA is a number of actions in the environment.
        theta: We stop evaluation once our value function change is less than theta for all states.
        discount_factor: Gamma discount factor.
    
    Returns:
        Vector of length env.nS representing the value function.
    """
    # Start with a random (all 0) value function    
    V_new = np.zeros(16)    
    # For each state, perform a "full backup"
    for s in range(16):
        v = 0.0
        # Look at the possible next actions
        for a, action_prob in list(enumerate(policy[s])):           
            # For each action, look at the possible next states...
            # Calculate the expected value
            nxt = next_state[s][a]
            # if not a barrier
            if(nxt != -1):
                v += action_prob * (reward + discount_factor * V_old[int(nxt)])            
        V_new[s] = v      
    
    return np.array(V_new)

def best_action(a):
    """
    Helper function to return the index of the best action according to action values. If there is more than 2 actions that have the same value then there is no best action
    Args:
        a: actions values  
        
    Returns:
        Best action index and returns -1 if there is a tie of 3 actions or more
    """
    if np.array_equal(a,[0,0,0,0]) or np.array_equal(a,[1,0,0,0])or np.array_equal(a,[0,1,0,0]) or np.array_equal(a,[0,0,1,0]) or np.array_equal(a,[0,0,0,1]):
        return np.argmax(a)
    freq = np.zeros(4)
    i=0
    while i<4: 
        j=0
        while j<4:
            if abs(a[i]-a[j]) < 0.00001:
                freq[i] += 1
            j+=1
        i+=1
    max_indx = np.argmax(a)
    if freq[max_indx]>2:
        return -1
    return np.argmax(a)

def policy_improvement(reward, next_state, goal_indx, policy_eval_fn=policy_eval, discount_factor=1.0):
    """
    Policy Improvement Algorithm. Iteratively evaluates and improves a policy
    until an optimal policy is found.
    
    Args:
        env: The OpenAI envrionment.
        policy_eval_fn: Policy Evaluation function that takes 3 arguments:
            policy, env, discount_factor.
        discount_factor: gamma discount factor.
        
    Returns:
        A tuple (policy, V). 
        policy is the optimal policy, a matrix of shape [S, A] where each state s
        contains a valid probability distribution over actions.
        V is the value function for the optimal policy.
        
    """

    def one_step_lookahead(state, V):
        """
        Helper function to calculate the value for all action in a given state.
        
        Args:
            state: The state to consider (int)
            V: The value to use as an estimator, Vector of length env.nS
        
        Returns:
            A vector of length env.nA containing the expected value of each action.
        """
        A = np.zeros(4)
        i=0
        for a in range(4):
            nxt = next_state[state][a]
            if(nxt != -1):
                A[i] += (reward + discount_factor * V[int(nxt)])
            i = i+1
        return A
    
    # Start with a random policy
    policy = np.ones([16, 4]) / 4    
    policy[goal_indx] = np.zeros(4)
    initial_policy = policy.copy()
    
    V_old = np.zeros(16)
    V_new = np.zeros(16)
    
    k=0
    while True:  
        print ("Iteration ",k,":")
        policy[goal_indx] = np.zeros(4)
        policy_old = policy.copy()
        # Evaluate the current policy       
        V_new = policy_eval_fn(initial_policy, reward, next_state, V_old)        
        V_old = V_new.copy()
        print("Cuurent Values:")
        print(V_new)
        # Will be set to false if we make any changes to the policy
        policy_stable = True
        
        # For each state...
        for s in range(16):
            # The best action we would take under the currect policy
            #chosen_a = np.argmax(policy[s])
            
            # Find the best action by one-step lookahead
            # Ties are resolved arbitarily
            action_values = one_step_lookahead(s, V_new)
            #best_a = np.argmax(action_values)
            best_a = best_action(action_values)
            
            # Greedily update the policy            
            #if chosen_a != best_a: 
            if(best_a == -1):
                policy_stable = False
            if(best_a != -1):
                policy[s] = np.eye(4)[best_a]
        # If the policy is stable we've found an optimal policy. Return it
        
        k+=1
        print("Current Policy Probability distribution: ")
        print(policy)
        if np.array_equal(policy,policy_old) and k>1 and is_deterministic(policy):
            return (policy, V_new)
        
def get_goal_indx(maze,N):
    """
    Finds the index of the goal state 'G'
    
    Args:
        maze: [N, N] shaped matrix representing the maze.
        N: Dimension of the maze
    
    Returns:
       Goal state 'G' index
    """
    s=0
    for i in range(N):
        for j in range(N):
            if maze[i][j] == 'G':
                return s
            s+=1
    return -1

N = 4
maze = [['S', '.', '.', '.'],
        ['#', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', 'G', '#', '.']]

reward = -1
discount_factor = 1.0
goal_index = get_goal_indx(maze,N) 
next_state = list(get_next_state(maze,N))
start_time = time.time()
policy, v = policy_improvement(reward, next_state , goal_index)
exec_time = (time.time() - start_time)
print("\n\n-------------Final Results---------\n\n-")
print("Policy Probability Distribution:")
print(policy)
print("")
print("Value Function:")
print(v)
print("")
path,actions = get_path_policy(policy)
print("Path: ")
print(path)
print("Actions: ")
print(actions)
print("--- Running Time : %s seconds ---" % exec_time)
