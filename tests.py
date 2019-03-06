# first test, test front turn
# test that original first row of front is same as
# new bot row of front in reverse, same for original
# last row and new
 
import unittest
from puzzle import State

def compareReverse(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[len(l1) - 1 - i]:
            print("lists from compareReverse... " + str(l1) + "  " + str(l2))
            return False
    return True

def compare(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            print(" lists from compare... " + str(l1) + "  " + str(l2))
            return False
    return True

class TestRotations(unittest.TestCase):

    def test_front_rotation(self):
        cube = State()
        # get three rows of front
        top_row = cube.front[0]
        bot_row = cube.front[2]
        mid_row = cube.front[1]
        top_first_row = cube.top[0]
        bot_first_row = cube.bottom[0]
        left_third_col = [cube.left[0][2],cube.left[1][2],cube.left[2][2]]
        right_first_col = [cube.right[0][0],cube.right[1][0],cube.right[2][0]]
        cube.turn_front()
        top_row2 = cube.front[0]
        top_first_row2 = cube.top[0]
        bot_first_row2 = cube.bottom[0]
        mid_row2 = cube.front[1]
        bot_row2 = cube.front[2]
        left_third_col2 = [cube.left[0][2],cube.left[1][2],cube.left[2][2]]
        right_first_col2 = [cube.right[0][0],cube.right[1][0],cube.right[2][0]]
        # check top row inverted and at bottom
        self.assertTrue(compareReverse(top_row, bot_row2))
        # check bot row inverted and at top
        self.assertTrue(compareReverse(bot_row, top_row2))
        # check mid row inverted in place
        self.assertTrue(compareReverse(mid_row, mid_row2))
        # check first top row move to first bot row
        self.assertTrue(compare(top_first_row, bot_first_row2))
        # check first bot row move to first top row
        self.assertTrue(compare(bot_first_row, top_first_row2))
        # check third col of left move to first col of right
        self.assertTrue(compareReverse(left_third_col, right_first_col2))
        # check first col of right move to third col of left
        self.assertTrue(compareReverse(right_first_col, left_third_col2))


if __name__ == "__main__":
    unittest.main()