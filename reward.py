def isGoalState(s):
    # check if all 3 lists that make up a side are equal
    # for every side, return false if this is not the case
    # e.g. side = [[1,1,1], [1,1,1], [1,1,2]]
    for side in s:
        num = side[0][0]
        # check if all values in each row are equal
        # to the first value
        for row in side:
            if not num == row[0] == row[1] == row[2]:
                return False
    return True

# returns reward for given state action pair
def reward(s, a):
    # TODO: implement action function for given state, that returns
    # state after completing action
    if isGoalState(action(s, a)):
        return 100
    return -1