import random

rows = 0
reward = 0
columns = 0
epsilon = 0
discount_factor = 0

walls = []
terminal_states = []

actions = ['N', 'E', 'S', 'W']
action_probability_pair = {'forward': 0, 'left': 0, 'right': 0, 'backwards': 0 }


'''
prints the grid
'''
def print_grid(rows, columns, grid):
    for i in range(0, columns):
        idx = columns - i - 1
        temp = '    '
        while(idx < columns * rows):
            temp += str(grid[idx])
            temp += '    '
            idx += columns
        print(temp)
        print('\n')

'''
function to find wall and terminals states
set '-' for wall states
set 'T' for terminal states
'''
def set_policy(cur_grid):
    list_move = []

    for i in cur_grid.states:

        if(cur_grid.if_wall(i)):
            list_move.append('-')

        elif(cur_grid.if_terminal(i)):
            list_move.append('T')
        else:
            list_move.append('')

    return list_move

'''
build the grid
'''
def build_grid(rows, columns):
    return [[(i // columns)+1 if(i % columns) else (i//columns), (i % columns) if(i % columns) else columns] for i in range(1, (rows * columns) + 1)] 

'''
return the current index
'''
def return_idx(state, columns):
    [row, col] = state
    return (row - 1) * columns + (col - 1)


'''
class definition for MDP
'''
class MDP:
    def __init__(self, states, actions, cur_environment, rewardFunc):
        self.states = states
        self.actions = actions
        self.cur_environment = cur_environment
        self.rewardFunc = rewardFunc

'''
Class definition for reward
set reward for each element
'''
class Reward:
    states = []
    rewards = {}

    @classmethod
    def set_reward(cur, states, terminal_states, reward):
        cur.states = states
        for state in cur.states:
            cur.rewards[''.join(str(el) for el in state)] = reward
        for i in terminal_states:
            cur.rewards[''.join(str(el) for el in i['state'])] = i['reward']
    
    @classmethod
    def get_reward(cur, state):
        return cur.rewards[''.join(str(el) for el in state)]


'''
Class definition for Utility

'''
class Utility: 
    def __init__(self, states, values):
        self.states = states
        self.values = values   
        
    def get_value(self, state, cur_idx):
        return self.values[cur_idx]

    def set_value(self, state, cur_idx, value):
        self.values[cur_idx] = value

    def get_all_values(self):
        return self.values

'''
Class definition for Policy
'''
class Policy:
    def __init__(self, policy, states):
        self.policy = policy
        self.states = states

    def set_policy(self, state, cur_idx, action):
        self.policy[cur_idx] = action

    def get_policy(self, state, cur_idx):
        return self.policy[cur_idx]

    def get_all_policy(self):
        return self.policy

'''
class definition for the current environment
'''
class Environment:
    def __init__(self, states, actions, walls, terminal_states, probabilities, rows, columns):
        self.states = states
        self.actions = actions
        self.rows = rows
        self.columns = columns
        self.walls = walls
        self.terminal_states = terminal_states
        self.forward = probabilities['forward']
        self.left = probabilities['left']
        self.right = probabilities['right']
        self.backwards = probabilities['backwards']
        self.wall_or_terminal = self.check_if_wall_or_terminal_states()

    
    '''
    helper for check_if_wall_or_terminal_states
    '''

    def if_wall(self, cur_idx):
        isnext_action_listsWall = False
        for wall in self.walls:
            if(wall[0] == cur_idx[0] and wall[1] == cur_idx[1]):
                isnext_action_listsWall = True
                break
        return isnext_action_listsWall

    '''
    helper for check_if_wall_or_terminal_states
    '''
    def if_terminal(self, cur_idx):
        if_terminal = False
        for i in self.terminal_states:
            if(i['state'][0] == cur_idx[0] and i['state'][1] == cur_idx[1]):
                if_terminal = True
                break
        return if_terminal

    '''
    function that looks for wall/terminal states
    '''
    def check_if_wall_or_terminal_states(self):
        wall_terminal_list = []
        for i in self.states:
            if(not(self.if_wall(i)) and not(self.if_terminal(i))):
                wall_terminal_list.append(i)
        return wall_terminal_list

    '''
    function that returns list of action to be performed
    '''
    def next_action_lists(self, cur, action):
        
        next_action_list = []
        cur_index = self.actions.index(action)

        forward_index = action

        if(cur_index == 0):
            left_index = self.actions[len(self.actions) - 1]
            right_index = self.actions[cur_index + 1]

        elif(cur_index == len(self.actions) - 1):
            left_index = self.actions[cur_index - 1]
            right_index = self.actions[0]

        else:
            left_index = self.actions[cur_index - 1]
            right_index = self.actions[cur_index + 1]
       
        next_action_list.append({'state': self.after_action_grid(cur, forward_index),'probability': self.forward});
        next_action_list.append({'state': self.after_action_grid(cur, left_index), 'probability': self.left });
        next_action_list.append({'state': self.after_action_grid(cur, right_index), 'probability': self.right});

        return next_action_list
    

    '''
    returns new grid after action
    '''
    def after_action_grid(self, state, action):
        [row, col] = state
        cur_idx = return_idx(state, self.columns)
        after_action_grid = []
        if(action == 'N'):
            if(col == self.columns or self.if_wall(self.states[cur_idx + 1])):
                after_action_grid = [state[0], state[1]]
            else:
                after_action_grid = [self.states[cur_idx + 1][0], self.states[cur_idx + 1][1]]
        elif(action == 'S'):
            if(col == 1 or self.if_wall(self.states[cur_idx - 1])):
                after_action_grid = [state[0], state[1]]
            else:
                after_action_grid = [self.states[cur_idx - 1][0], self.states[cur_idx - 1][1]]
        elif(action == 'E'):
            if(row == self.rows or self.if_wall(self.states[cur_idx + self.columns])):
                after_action_grid = [state[0], state[1]]
            else:
                after_action_grid = [self.states[cur_idx + self.columns][0], self.states[cur_idx + self.columns][1]]
        elif(action == 'W'):
            if(row == 1 or self.if_wall(self.states[cur_idx - self.columns])):
                after_action_grid = [state[0], state[1]]
            else:
                after_action_grid = [self.states[cur_idx - self.columns][0], self.states[cur_idx - self.columns][1]]
        else:
            after_action_grid = [state[0], state[1]]
        
        return after_action_grid



'''
Function that performs value iteration

'''
def value_iteration(mdp, epsilon, discount_factor):

    iteration = 0
    value_iter = {}
    values = [0 for each in mdp.states]
    utility = Utility(mdp.states, values)

    '''
    helper to calculate 
    value after action
    '''
    def cur_value(mdp, state, action, utility, discount_factor):
        total_val = 0
        for i in mdp.cur_environment.next_action_lists(state, action):
            total_val += i['probability'] * ( mdp.rewardFunc(i['state']) + ( discount_factor * utility.get_value(i['state'], return_idx(i['state'], mdp.cur_environment.columns)) ))
        return total_val

    
    while(True):

        print('<---------------------------------------- ITERATION: ' + str(iteration) + '----------------------------------------> \n')
        print_grid(mdp.cur_environment.rows, mdp.cur_environment.columns, utility.get_all_values())
        print('\n')

        if(iteration == 20000):
            print("i give up asdfghjdhgsfdf--------------------\n")
            return

        iteration = iteration+1
        values = [value for value in utility.get_all_values()]
        value_iter = Utility(mdp.states, values)

        '''
        iterate over each state
        perform every possible action
        find max eward
        set max difference
        '''
        for i in mdp.cur_environment.wall_or_terminal:
            max_diff = 0
            value_list = []

            for j in mdp.actions:
                value_list.append(cur_value(mdp, i, j, value_iter, discount_factor))
            maxNewValue = max(value_list)
            cur_idx = return_idx(i, mdp.cur_environment.columns)
            utility.set_value(i, cur_idx, maxNewValue)
            
            if (abs(utility.get_value(i, cur_idx) - value_iter.get_value(i, cur_idx)) > max_diff):
                max_diff = abs(utility.get_value(i, cur_idx) - value_iter.get_value(i, cur_idx))

        # base case
        if(max_diff < ((epsilon * (1 - discount_factor))/discount_factor) ):
            break

    return value_iter

'''
Function that returns
value depending on policy
'''
def value_depends_policy(mdp, state, policy, utility, discount_factor):
    total_val = 0
    cur_idx = return_idx(state, mdp.cur_environment.columns)
    action = policy.get_policy(state, cur_idx)
    for i in mdp.cur_environment.next_action_lists(state, action):
        total_val += i['probability'] * ( mdp.rewardFunc(i['state']) + ( discount_factor * utility.get_value(i['state'], return_idx(i['state'], mdp.cur_environment.columns)) ))
    return total_val

'''
Function that returns
the best action to take
'''
def max_reward(state, actions, cur_environment, utility, rewardFunc, discount_factor):
    list_values = []
    for i in actions:
        total_value = 0
        for j in cur_environment.next_action_lists(state, i):
            total_value += j['probability'] * ( rewardFunc(j['state']) + (discount_factor * utility.get_value(j['state'], return_idx(j['state'], cur_environment.columns)) ))
        list_values.append(total_value)
    best_reward_action = list_values.index(max(list_values))
    return actions[best_reward_action]


'''
performs policy iteration
takes mdp, discount factor as input
calculate probability for every move
'''
def policy_iteration(mdp, discount_factor):
    list_moves = set_policy(mdp.cur_environment)
    for i in range(0, len(list_moves)):
        list_moves[i] = mdp.actions[random.randrange(0, len(mdp.actions))] if(list_moves[i] == '') else list_moves[i]
    
    '''
    helper for policy iteration
    '''
    def helper_policy_iteration(policy, utility, mdp, discount_factor, k):
        for i in range(k):
            for j in mdp.cur_environment.wall_or_terminal:
                state_idx = return_idx(j, mdp.cur_environment.columns)
                utility.set_value(j, state_idx, value_depends_policy(mdp, j, policy, utility, discount_factor))
        return utility

    policy = Policy(list_moves, mdp.states)
    utility = Utility(mdp.states, [0 for s in mdp.states])
    while(True):
        utility = helper_policy_iteration(policy, utility, mdp, discount_factor, 20)
        diff = True

        '''
        helper to calculate probability depending on move
        returns best action to take
        '''
        def max_reward(state, actions, cur_environment, utility, rewardFunc, discount_factor):
            list_values = []
            for i in actions:
                total_value = 0
                for next_action_lists in cur_environment.next_action_lists(state, i):
                    total_value += next_action_lists['probability'] * ( rewardFunc(next_action_lists['state']) + (discount_factor * utility.get_value(next_action_lists['state'], return_idx(next_action_lists['state'], cur_environment.columns)) ))
                list_values.append(total_value)
            return actions[list_values.index(max(list_values))]


        for i in mdp.cur_environment.wall_or_terminal:
            action = max_reward(i, mdp.actions, mdp.cur_environment, utility, Reward.get_reward, discount_factor)

            cur_idx = return_idx(i, mdp.cur_environment.columns)
            if(action != policy.get_policy(i, cur_idx)):
                policy.set_policy(i, cur_idx, action)
                diff = False

        if(diff):
            return policy


'''
main function
takes filename input from user
calls mdp
print mdp results
'''
def main():

    filename = input("Enter filename: \n")
    # filename = "mdp_input_book.txt"
    # filename = "mdp_input.txt"

    # read and parse data from input file
    with open(filename,'r') as f:
        line = f.readlines()
        rows = int("".join(line[2].split()).split(":")[1][0])
        columns = int("".join(line[2].split()).split(":")[1][1])

        # find wall
        find_wall = "".join(line[6].split()).split(":")[1].split(",")
        for i in find_wall:
            walls.append([int(i[0]), int(i[1])])


        # find terminal states
        find_terminal_states = "".join(line[10].split()).split(":")[1].split(",")
        for i in find_terminal_states:
            terminal_states.append({
                'state': [int(i[0]), int(i[1])],
                'reward': 0 + float(i[2] + i[3])
            })

        # calculate probability
        probability = []
        for i in " ".join(line[18].split()).split(":")[1].split(" "):
            if(i != ""):
                probability.append(i)
        action_probability_pair['forward'] = float(probability[0])
        action_probability_pair['left'] = float(probability[1])
        action_probability_pair['right'] = float(probability[2])
        action_probability_pair['backwards'] = float(probability[3])

        reward = float("".join(line[14].split()).split(":")[1])
        discount_factor = float("".join(line[20].split()).split(":")[1])
        epsilon = float("".join(line[22].split()).split(":")[1])

    intial_grid = build_grid(rows, columns)
    Reward.set_reward(intial_grid, terminal_states, reward)
    
    cur_environment = Environment(intial_grid, 
                            actions, 
                            walls, 
                            terminal_states, 
                            action_probability_pair, 
                            rows, 
                            columns)

    mdp = MDP(intial_grid, actions, cur_environment, Reward.get_reward)

    # set reward value for certain state
    utility = value_iteration(mdp, epsilon, discount_factor)
    intial_policy = set_policy(cur_environment)
    policy = Policy(intial_policy, intial_grid)

    for state in cur_environment.wall_or_terminal:
        cur_idx = return_idx(state, cur_environment.columns)
        policy.set_policy(state, cur_idx, max_reward(state, actions, cur_environment, utility, Reward.get_reward, discount_factor))



    # print the values with value iteration
    print("<---------------------------------------- FINAL VALUE AFTER CONVERGENCE ----------------------------------------> \n")
    print_grid(rows, columns, utility.get_all_values())

    # print the policy with value iteration
    print("<---------------------------------------- FINAL POLICY ----------------------------------------> \n")
    print_grid(rows, columns, policy.get_all_policy())
    policyWithPI = policy_iteration(mdp, discount_factor)

    # print the policy after modified policy iteration
    print("<---------------------------------------- POLICY ITERATION ----------------------------------------> \n")
    print_grid(rows, columns, policyWithPI.get_all_policy())


if __name__ == "__main__":
    main()
