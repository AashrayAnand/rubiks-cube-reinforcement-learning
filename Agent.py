import random, time
from puzzle import State, move, num_solved_sides, num_pieces_correct_side, shuffle, six_move_state, one_move_state

ALPHA = 0.5

    # q-values key = (state, action) => value = (q-value, update_count)
class Agent:

    # initialize agent, can be passed a dictionary of Q-Values
    # if it already exists, and a cube, otherwise, initializes new
    # cube if not provided one
    def __init__(self, QValues=None, cube=None):
        self.visited = []
        self.visit_count = {}
        self.revisits = 0
        # maps a state action pair to a Q-Value, and an update count for that Q-Value
        self.QV = QValues if QValues is not None else {}
        # maps a state to a list of rewards for executing each possible outcome
        # can index list of rewards using directional class constants
        self.R = {}
        # create or store initial cube state, and store list of actions
        self.start_state = cube if cube is not None else six_move_state() #six_move_state()
        print(self.start_state)
        time.sleep(5)
        # shuffle initially solved starting state, executing 5 random moves
        # self.start_state = shuffle(self.start_state)
        # store the current state
        self.curr_state = self.start_state
        self.prev_state = None
        self.second_last_action = None
        self.actions = self.start_state.actions
        self.last_action = None
        self.move = {"front": 0, "back": 0, "left": 0, "right": 0, "top": 0, "bottom": 0}

    # explore
    def QLearn(self, discount=0.99, episodes=5, epsilon=0.9):
        # execute q learning for specified number of episodes
        self.curr_state = self.start_state
        for i in range(episodes):
            print("=====EPISODE "+str(i)+"=====")
            print("====CURR STATE========")
            print("======================")
            # initialize values in Q-State dictionary for 
            # any state action pairs including current state
            # that are null
            saved_rewards = self.curr_state.__hash__() in self.R.keys()
            if not saved_rewards:
                self.R[self.curr_state.__hash__()] = []
            if not self.curr_state.__hash__ in self.visit_count:
                self.visit_count[self.curr_state.__hash__()] = 1
            else:
                self.visit_count[self.curr_state.__hash__()] += 1
            vc = self.visit_count[self.curr_state.__hash__()]
            # initialize Q-Values of 0 for all state action pairs
            # for the given, state, if they do not exist
            for action in self.actions:
                if not (self.curr_state.__hash__(), action) in self.QV.keys():
                    self.QV[(self.curr_state.__hash__(), action)] = 0
                else:
                    self.revisits += 1
                    break
                if not saved_rewards:
                    self.R[self.curr_state.__hash__()].append(self.reward(self.curr_state, action))
            follow_policy = random.uniform(0,1.0)
            print("random value generated is " + str(follow_policy))
            # if random number is > epsilon, we must select best move
            # by the highest q-value
            if follow_policy > epsilon:
                print("FOLLOWING POLICY")
                for action in self.actions:
                    print("q value for action " + action + " from curr state is " + str(self.QV[(self.curr_state.__hash__(), action)]))
                best_action = None
                best_QV = -100000000
                for action in self.actions:
                    if self.QV[(self.curr_state.__hash__(), action)] > best_QV and action != self.last_action:
                        best_action = action
                        best_QV = self.QV[(self.curr_state.__hash__(), action)]
                if best_QV == 0:
                    best_action = random.choice(self.actions)
                    while best_action == self.last_action:
                        best_action = random.choice(self.actions)
                print("actions chosen = " + best_action)
                self.move[best_action] = self.move[best_action] + 1
                # update Q-Value for current state and action chosen based on the current policy, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                #reward = self.reward(self.curr_state, best_action)
                #max_reward = self.max_reward(self.curr_state, best_action)
                #self.QV[(self.curr_state.__hash__(), best_action)] = best_QV + ALPHA*(reward +\
                #                                         discount*max_reward - best_QV)
                for action in self.actions:
                    curr_QV = self.QV[(self.curr_state.__hash__(), action)]
                    reward = self.reward(self.curr_state, action)
                    max_reward = self.max_reward(self.curr_state, action)
                    self.QV[(self.curr_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
                                                         (discount**vc)*max_reward - curr_QV)
                print("new q value for " + best_action + " action is " + str(self.QV[(self.curr_state.__hash__(), best_action)]))
                self.curr_state.move(best_action)
                self.curr_state = self.curr_state.copy()
                if self.curr_state.isGoalState():
                    print("reached goal state while in Q-learning epsiode " + str(i))
                    time.sleep(2)
                    return
                self.second_last_action = self.last_action  
                self.last_action = best_action
            else:
                # pick random move
                action = random.choice(self.actions)
                self.move[action] = self.move[action] + 1
                while action == self.last_action:
                    action = random.choice(self.actions)
                # update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                #reward = self.reward(self.curr_state, action)
                #max_reward = self.max_reward(self.curr_state, action)
                #print("max reward... " + str(max_reward))
                #print("reward... " + str(reward))
                #self.QV[(self.curr_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
                #                                    discount*max_reward - curr_QV)
                for action in self.actions:
                    curr_QV = self.QV[(self.curr_state.__hash__(), action)]
                    reward = self.reward(self.curr_state, action)
                    max_reward = self.max_reward(self.curr_state, action)
                    self.QV[(self.curr_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
                                                         (discount**vc)*max_reward - curr_QV)
                #print(self.reward(self.curr_state,action))
                #print(self.QV[(self.curr_state,action)])
                self.curr_state.move(action)
                self.curr_state = self.curr_state.copy()
                self.second_last_action = self.last_action  
                self.last_action = action

    def Play(self):
        self.curr_state = self.start_state
        for i in range(10):
            best_action = None
            best_QV = -100000000
            if not (self.curr_state.__hash__(), self.actions[0]) in self.QV.keys():
                best_action = random.choice(self.actions)
                while best_action == self.last_action:
                    best_action = random.choice(self.actions)
                for action in self.actions:
                    self.QV[(self.curr_state.__hash__(), action)] = 0
                best_QV = 0
            else:
                for action in self.actions:
                    if self.QV[(self.curr_state.__hash__(), action)] > best_QV and action != self.last_action:
                        best_action = action
                        best_QV = self.QV[(self.curr_state.__hash__(), action)]
                if best_QV == 0:
                    best_action = random.choice(self.actions)
                    while best_action == self.last_action or best_action == self.second_last_action:
                        best_action = random.choice(self.actions)
            print("actions chosen = " + best_action)
            print("last action = " + self.last_action)
            print("q value is " + str(self.QV[(self.curr_state.__hash__(), best_action)]))
            time.sleep(1)
            self.curr_state.move(action)
            self.last_action = best_action
            print(self.curr_state)
            if self.curr_state.isGoalState():
                print("HOLY SHIT")
                time.sleep(5)
                return


    def printQV(self):
        print("=============")
        x = 0
        y = 0
        for key in self.QV.keys():
            if self.QV[key] != 0:
                x += 1
            else:
                y += 1
        print("number of q values in dictionary is " + str(x + y))
        print("number of q values with zero value is " + str(y))
        print("number of q value with non zero value is " + str(x))
        print("number of re visits = " + str(self.revisits))
        values = []
        for key in self.QV.keys():
            if self.QV[key] != 0:
                values.append(self.QV[key])
        print(values)
        print(self.move)
            
    def reward(self, state, action):
        # this reward function should be a function approximation made up of 
        # a set of features, these features should be in decreasing order of priority:
        # 1. solved sides ()
        # use next state to get value for next state vs. self.curr_state, to determine
        # if feature values should be 1 or 0, e.g. if solved_sides(next_state) > solved_sides(self.curr_state)
        # then the solved sides feature is 1, else 0
        next_state = move(state, action)
        if next_state.isGoalState():
            print(state)
            print(next_state)
            print("REWARD IS GOAL")
            time.sleep(3)
            return 100
        #new_state = move(state, action)
        reward = 0
        solved_sides = num_solved_sides(next_state)
        reward += 7*solved_sides
        reward += num_pieces_correct_side(next_state)
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
for i in range(100):
    print("======= ROUND " + str(i) + "=========")
    agent.QLearn()
print("there are " + str(len(agent.QV)) + " keys in Q Table")
#agent.QLearn(epsilon=0.1)
agent.Play()
agent.printQV()