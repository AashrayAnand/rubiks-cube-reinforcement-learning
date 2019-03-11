import random, time
from puzzle import State, move, num_solved_sides, num_pieces_correct_side, shuffle, ten_move_state

FRONT = 0
BACK = 1
LEFT = 2
RIGHT = 3
TOP = 4
BOTTOM = 5
ALPHA = 0.3

    # q-values key = (state, action) => value = (q-value, update_count)
class Agent:

    # initialize agent, can be passed a dictionary of Q-Values
    # if it already exists, and a cube, otherwise, initializes new
    # cube if not provided one
    def __init__(self, QValues=None, cube=None):
        self.visited = set()
        self.ordered_quality = []
        # maps a state action pair to a Q-Value, and an update count for that Q-Value
        self.QV = QValues if QValues is not None else {}
        # maps a state to a list of rewards for executing each possible outcome
        # can index list of rewards using directional class constants
        self.R = {}
        # create or store initial cube state, and store list of actions
        self.start_state = cube if cube is not None else ten_move_state()
        # shuffle initially solved starting state, executing 5 random moves
        self.start_state = shuffle(self.start_state)
        # store the current state
        self.curr_state = self.start_state
        self.actions = self.start_state.actions
        self.last_action = None
        self.move = {"front": 0, "back": 0, "left": 0, "right": 0, "top": 0, "bottom": 0}

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
                print("FOLLOWING POLICY")
                for action in self.actions:
                    print("q value for action " + action + "from curr state is " + str(self.QV[(self.curr_state, action)]))
                    time.sleep(1)
                time.sleep(2)
                best_action = None
                best_QV = -100000000
                for action in self.actions:
                    if self.QV[(self.curr_state, action)] > best_QV and action != self.last_action:
                        best_action = action
                        best_QV = self.QV[(self.curr_state, action)]
                self.move[best_action] = self.move[best_action] + 1
                # update Q-Value for current state and action chosen based on the current policy, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                max_reward = self.max_reward(self.curr_state, best_action)
                reward = self.reward(self.curr_state, best_action)
                self.QV[(self.curr_state, best_action)] = best_QV + ALPHA*(reward +\
                                                         discount*max_reward - best_QV)
                self.ordered_quality.append((self.QV[(self.curr_state, best_action)], self.curr_state))
                self.curr_state.move(best_action)
                self.last_action = best_action
                #self.ordered_quality.put((self.QV[(self.curr_state, best_action)], str(self.curr_state)))
            else:
                # pick random move
                action = random.choice(self.actions)
                self.move[action] = self.move[action] + 1
                while action == self.last_action:
                    action = random.choice(self.actions)
                curr_QV = self.QV[(self.curr_state, action)]
                # update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                max_reward = self.max_reward(self.curr_state, action)
                reward = self.reward(self.curr_state, action)
                self.QV[(self.curr_state, action)] = curr_QV + ALPHA*(reward +\
                                                    discount*max_reward - curr_QV)
                #print(self.reward(self.curr_state,action))
                #print(self.QV[(self.curr_state,action)])
                self.ordered_quality.append((self.QV[(self.curr_state, action)], self.curr_state))
                self.curr_state.move(action)
                self.last_action = action


    def printQV(self):
        for i in range(10):
            print(self.ordered_quality[i][0])
            print(self.ordered_quality[i][1])
            print(len(self.QV.keys()))
        print(self.move)
            
    def reward(self, state, action):
        new_state = move(state, action)
        reward = 0
        solved_sides = num_solved_sides(new_state)
        reward += 7*solved_sides
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