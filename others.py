from puzzle import State, move

def makeNearGoal():
    cube = State()
    cube.set_top([['W','W','W'],['W','W','W'],['W','W','W']])
    cube.set_bottom([['B','B','B'],['B','B','B'],['B','B','B']])
    cube.set_left([['O','O','O'],['G','G','G'],['G','G','G']])
    cube.set_right([['G','G','G'],['O','O','O'],['O','O','O']])
    cube.set_front([['R','R','R'],['Y','Y','Y'],['Y','Y','Y']])
    cube.set_back([['Y','Y','Y'],['R','R','R'],['R','R','R']])
    for action in cube.actions:
        new_s = move(cube, action)
        print(action)
        if new_s.isGoalState():
            print("executing the " + action + " action resulted in the below goal state " + str(new_s))
    #print(cube)    
   #print(move(cube, 'top'))
        

        

makeNearGoal()