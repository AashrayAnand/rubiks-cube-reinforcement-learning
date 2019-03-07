import random, time
from puzzle import State, move, num_solved_sides, num_pieces_correct_side

FRONT = 0
BACK = 1
LEFT = 2
RIGHT = 3
TOP = 4
BOTTOM = 5
ALPHA = 0.3
from queue import PriorityQueue


    # q-values key = (state, action) => value = (q-value, update_count)
class Agent:

    # initialize agent, can be passed a dictionary of Q-Values
    # if it already exists, and a cube, otherwise, initializes new
    # cube if not provided one
    def __init__(self, QValues=None, cube=None):
        self.visited = set()
        self.ordered_quality = PriorityQueue()
        # maps a state action pair to a Q-Value, and an update count for that Q-Value
        self.QV = QValues if QValues is not None else {}
        # maps a state to a list of rewards for executing each possible outcome
        # can index list of rewards using directional class constants
        self.R = {}
        # create or store initial cube state, and store list of actions
        self.start_state = cube if cube is not None else State()
        self.curr_state = self.start_state
        self.actions = ['front', 'back', 'left', 'right', 'top', 'bottom']
        self.last_action = None

    # explore
    def QLearn(self, discount=0.99, episodes=1000, epsilon=0.9):
        # execute q learning for specified number of episodes
        for i in range(episodes):
            print("=====EPISODE "+str(i)+"=====")
            print("====CURR STATE========")
            self.visited.add(self.curr_state)
            print("======================")
            # initialize values in Q-State dictionary for 
            # any state action pairs including current state
            # that are null
            saved_rewards = self.curr_state in self.R.keys()
            if not saved_rewards:
                self.R[self.curr_state] = []
            # initialize Q-Values of 0 for all state action pairs
            # for the given, state, if they do not exist
            for action in self.actions:
                if not (self.curr_state, action) in self.QV.keys():
                    self.QV[(self.curr_state, action)] = 0
                if not saved_rewards:
                    self.R[self.curr_state].append(self.reward(self.curr_state, action))
            follow_policy = random.uniform(0,1.0)
            print("random value generated is " + str(follow_policy))
            # if random number is > epsilon, we must select best move
            # by the highest q-value
            if follow_policy > epsilon:
                best_action = None
                best_QV = -100000000
                for action in self.actions:
                    if self.QV[(self.curr_state, action)] > best_QV and action != self.last_action:
                        best_action = action
                        best_QV = self.QV[(self.curr_state, action)]
                # update Q-Value for current state and action chosen based on the current policy, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                self.QV[(self.curr_state, best_action)] = best_QV + ALPHA*(self.reward(self.curr_state, best_action) +\
                                                         discount*self.max_reward(self.curr_state, best_action) - best_QV)
                self.ordered_quality.put(self.QV[(self.curr_state, action)])
                self.curr_state = move(self.curr_state, best_action)
                self.last_action = best_action
                #self.ordered_quality.put((self.QV[(self.curr_state, best_action)], str(self.curr_state)))
            else:
                # pick random move
                action = random.choice(self.actions)
                while action == self.last_action:
                    action = random.choice(self.actions)
                curr_QV = self.QV[(self.curr_state, action)]
                # update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                self.QV[(self.curr_state, action)] = curr_QV + ALPHA*(self.reward(self.curr_state, action) +\
                                                    discount*self.max_reward(self.curr_state, action) - curr_QV)
                if self.reward(self.curr_state, action) != 0:
                    print(self.reward(self.curr_state,action))
                    print(self.QV[(self.curr_state,action)])
                    time.sleep(3)
                self.curr_state = move(self.curr_state, action)
                self.last_action = action
                #self.ordered_quality.put((self.QV[(self.curr_state, action)], str(self.curr_state)))
    def printQV(self):
        for i in range(10):
            print(self.ordered_quality.get())
            
    def reward(self, state, action):
        new_state = move(state, action)
        reward = 0
        reward += 15*num_solved_sides(new_state)
        reward += num_pieces_correct_side(new_state)
        return reward

    def max_reward(self, state, action):
        new_state = move(state, action)
        if not new_state in self.R.keys():
            self.R[new_state] = []
            for action in self.actions:
                self.R[new_state].append(self.reward(new_state, action))
        return max(self.R[new_state])
    # execute Q-value iteration

    # run based on current policy

agent = Agent()
agent.QLearn()
agent.printQV()