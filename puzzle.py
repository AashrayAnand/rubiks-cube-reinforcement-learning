from random import shuffle
SIDES = 6
# state object
class State:
    def __init__(self, size=3, c=None):
        self.size = size
        if c:
            self.__front__ = c["front"]
            self.__back__ = c["back"]
            self.__left__ = c["left"]
            self.__right__ = c["right"]
            self.__top__ = c["top"]
            self.__bottom__ = c["bottom"]
            self.__sides__ = [self.__front__, self.__back__, self.__left__, self.__right__, self.__top__, self.__bottom__]
            return
        # create array of values 1-6 for different colors
        # and multiply by number of pieces per size to get
        # equal amount of each color (white. black, red, orange, green, yellow)
        nums = ['W','B','R','O','G','Y']*(size**2)
        # shuffle numbers
        shuffle(nums)
        front, nums = nums[0:size**2],nums[size**2:]
        self.__front__ = [front[i:i + size] for i in range(0,len(front), size)]
        back, nums = nums[0:size**2],nums[size**2:]
        self.__back__ = [back[i:i + size] for i in range(0,len(front), size)]
        left, nums = nums[0:size**2],nums[size**2:]
        self.__left__ = [left[i:i + size] for i in range(0,len(front), size)]
        right, nums = nums[0:size**2],nums[size**2:]
        self.__right__ = [right[i:i + size] for i in range(0,len(front), size)]
        top, nums = nums[0:size**2],nums[size**2:]
        self.__top__ = [top[i:i + size] for i in range(0,len(front), size)]
        bottom, nums = nums[0:size**2],nums[size**2:]
        self.__bottom__ = [bottom[i:i + size] for i in range(0,len(front), size)]
        self.__sides__ = [self.__front__, self.__back__, self.__left__, self.__right__, self.__top__, self.__bottom__]

    # return new copy of State
    def copy(self):
        sides = {"front": self.__front__, "back": self.__back__, "left": self.__left__,\
                 "right": self.__right__, "top": self.__top__, "bottom": self.__bottom__}
        new_State = State(c=sides)
        return new_State

    # equality tested for cube
    def eq(self, other):
        return self.__left__ == other.left() and self.__right__ == other.right()\
                and self.__top__ == other.top() and self.__bottom__ == other.bottom()\
                and self.__front__ == other.front() and self.__back__ == other.back()

    # getters for cube sides
    def left(self):
        return self.__left__
    def right(self):
        return self.__right__
    def top(self):
        return self.__top__
    def bottom(self):
        return self.__bottom__
    def front(self):
        return self.__front__
    def back(self):
        return self.__back__

    # stringify a cube
    def __str__(self):
        return "\nFRONT" + str(self.__front__) + "\nBACK" + str(self.__back__) + "\nLEFT" \
        + str(self.__left__) + "\nRIGHT" + str(self.__right__) + "\nTOP" + str(self.__top__) + "\nBOTTOM" + str(self.__bottom__)
    
    # execute a 180 degreee clockwise rotation of a given side
    def rotate_side(self, side):
        new_side = [[],[],[]]
        for i in reversed(range(self.size)):
            for y in range(self.size):
                new_side[self.size - 1 - i].append(side[i][self.size - 1 - y])
        return new_side

    # modify a side, rotating its rows to columns, either in left to right
    # or right to left order, depending on the reverse parameter
    def columns_to_rows(self, side, reverse=False):
        new_side = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # left to right order
                if not reverse:
                    row.append(side[self.size - 1 - j][i])
                # right to left order
                else:
                    row.append(side[j][self.size - 1 - i])
            new_side.append(row)
        return new_side

    # rotate the cube 90 degrees counter clockwise
    def rotate_cube(self):
        left_side = self.__left__
        self.__left__ = self.replace_side(self.__back__)
        front_side = self.__front__
        self.__front__ = self.replace_side(left_side)
        right_side = self.__right__
        self.__right__ = self.replace_side(front_side)
        self.__back__ = self.replace_side(right_side)
        self.__top__ = self.columns_to_rows(self.__top__, reverse=True)
        self.__bottom__ = self.columns_to_rows(self.__bottom__)   
    
    # swap the first row of two given sides, in place
    def swap_first_row(self, side1, side2):
        s1_1 = side1[0]
        s2_1 = side2[0]
        # get rest of rows of side1
        new_side1 = [s2_1] + list(side for side in side1[1:])
        # get rest of rows of side2
        new_side2 = [s1_1] + list(side for side in side2[1:])
        return new_side1, new_side2
    
    # take the last element of each row of side 1, swap in place with
    # first element of reach row of side 2
    def swap_first_last_col(self, side1, side2):
        for i in range(len(side1)):
            side1[i][self.size - 1], side2[i][0] =  side2[i][0], side1[i][self.size - 1]
        return side1, side2

    # given a new side, return a copy of this side, 
    # to replace a given side of a cube
    def replace_side(self, side):
        new_side = []
        for row in side:
            new_side.append(row)
        return new_side
    
    # flip cube forward, from perspective of user looking at front
    # flipping such that front goes to bottom and top comes to front
    def flip_forward(self):
        front = self.__front__
        self.__front__ = self.replace_side(self.__top__)
        bottom = self.__bottom__
        self.__bottom__ = self.replace_side(front)
        back = self.__back__
        self.__back__ = self.replace_side(bottom)
        self.__top__ = self.replace_side(back)
    
    # flip cube backward, from perspective of user looking at front
    # flipping such that front goes to top and bottom goes to front
    def flip_backward(self):
        front = self.__front__
        self.__front__ = self.replace_side(self.__bottom__)
        top = self.__top__
        self.__top__ = self.replace_side(front)
        back = self.__back__
        self.__back__ = self.replace_side(top)
        self.__bottom__ = self.replace_side(back)
    
    # flip cube, either forward or backward, and invert
    # sides that must be inverted as a result
    def flip_cube(self, forward=False):
        # if flipping forward, we set front to be top
        # top to be back, back to be bottom, and bottom
        # to be front, we must then invert the back and front

        # if flipping backward, we set front to be bottom
        # top to be front, back to be top, and bottom to be
        # back, we must then invert the top and bottom
        if forward:
            self.flip_forward()
            self.__front__ = self.rotate_side(self.__front__)
            self.__back__ = self.rotate_side(self.__back__)
        else:
            self.flip_backward()
            self.__top__ = self.rotate_side(self.__top__)
            self.__bottom__ = self.rotate_side(self.__bottom__)


    # current move constraints: can only move clockwise
    # and can only turn the cube 180 degrees,
    # turn the front side to the right, causes the first
    # row of top/bottom to be swapped, and the first row of
    # left/right to be swapped, and the front face to be inverted
    # when we rotate a side, we are implementing it assuming that the
    # user turns their face to that side of the rubik's cube, then 
    # does a 180 degree left rotation, this simplifies the implementation

    def turn_front(self):
        # invert the front side
        self.__front__ = self.rotate_side(self.__front__)
        # swap the first row of the left/right side, and swap 
        # the last column of the left side with the first column of the right side
        self.__top__, self.__bottom__ = self.swap_first_row(self.__top__, self.__bottom__)
        self.__left__, self.__right__ = self.swap_first_last_col(self.__left__, self.__right__)
        
    def turn_back(self):
        # swap the last row of the left/right sides, and the first
        # row of the top/bottom sides
        # must rotate 90 degress twice
        self.rotate_cube()
        self.rotate_cube()
        self.turn_front

    
    def turn_left(self):
        # left become front, front becomes right, right becomes back, back becomes left
        # top gets rotated 90 degrees counter clockwise 
        # (3 6 9 -> 1 2 3) (2 5 8 -> 4 5 6) (1 4 7 -> 7 8 9)

        # must turn the cube 90 degrees counter clockwise to face the
        # left side of the cube, now as the front, then turn_front
        self.rotate_cube()
        self.turn_front()

    
    def turn_right(self):
        # must make 3 90 degree rotations of the cube for the right
        # side to face front
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()
        self.__right__ = self.rotate_side(self.__right__)
    
    def turn_top(self):
        self.flip_cube(forward=True)
        self.turn_front()
    
    def turn_bottom(self):
        self.flip_cube()
        self.turn_front()

    def isGoalState(self):
    # check if all 3 lists that make up a side are equal
    # for every side, return false if this is not the case
    # e.g. side = [[1,1,1], [1,1,1], [1,1,2]]
        for side in self.__sides__:
            num = side[0][0]
            # check if all values in each row are equal
            # to the first value
            for row in side:
                if not num == row[0] == row[1] == row[2]:
                    return False
        return True