from random import shuffle
SIDES = 6
# state object
class State:
    def __init__(self, size=3, c=None):
        self.size = size
        if c:
            self.front = c.front
            self.back = c.back
            self.left = c.left
            self.right = c.right
            self.top = c.top
            self.bottom = c.bottom
            return
        # create array of values 1-6 for different colors
        # and multiply by number of pieces per size to get
        # equal amount of each color (white. black, red, orange, green, yellow)
        nums = ['W','B','R','O','G','Y']*(size**2)
        # shuffle numbers
        shuffle(nums)
        front, nums = nums[0:size**2],nums[size**2:]
        self.front = [front[i:i + size] for i in range(0,len(front), size)]
        back, nums = nums[0:size**2],nums[size**2:]
        self.back = [back[i:i + size] for i in range(0,len(front), size)]
        left, nums = nums[0:size**2],nums[size**2:]
        self.left = [left[i:i + size] for i in range(0,len(front), size)]
        right, nums = nums[0:size**2],nums[size**2:]
        self.right = [right[i:i + size] for i in range(0,len(front), size)]
        top, nums = nums[0:size**2],nums[size**2:]
        self.top = [top[i:i + size] for i in range(0,len(front), size)]
        bottom, nums = nums[0:size**2],nums[size**2:]
        self.bottom = [bottom[i:i + size] for i in range(0,len(front), size)]


    # cube is represented in side order:
    # front, back, left, right, top, bottom
    def __str__(self):
        return "\nFRONT" + str(self.front) + "\nBACK" + str(self.back) + "\nLEFT" \
        + str(self.left) + "\nRIGHT" + str(self.right) + "\nTOP" + str(self.top) + "\nBOTTOM" + str(self.bottom)
    
    def rotate_side(self, side):
        new_side = [[],[],[]]
        for i in reversed(range(self.size)):
            for y in range(self.size):
                new_side[self.size - 1 - i].append(side[i][self.size - 1 - y])
        return new_side

    def columns_to_rows(self, side, reverse=False):
        new_side = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if not reverse:
                    row.append(side[self.size - 1 - j][i])
                else:
                    row.append(side[j][self.size - 1 - i])
            new_side.append(row)
        return new_side

    def rotate_cube(self):
        left_side = self.left
        self.left = self.replace_side(self.back)
        front_side = self.front
        self.front = self.replace_side(left_side)
        right_side = self.right
        self.right = self.replace_side(front_side)
        self.back = self.replace_side(right_side)
        self.top = self.columns_to_rows(self.top, reverse=True)
        self.bottom = self.columns_to_rows(self.bottom)   
    
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

    def replace_side(self, side):
        new_side = []
        for row in side:
            new_side.append(row)
        return new_side
    
    def flip_forward(self):
        front = self.front
        self.front = self.replace_side(self.top)
        bottom = self.bottom
        self.bottom = self.replace_side(front)
        back = self.back
        self.back = self.replace_side(bottom)
        self.top = self.replace_side(back)
    
    def flip_backward(self):
        front = self.front
        self.front = self.replace_side(self.bottom)
        top = self.top
        self.top = self.replace_side(front)
        back = self.back
        self.back = self.replace_side(top)
        self.bottom = self.replace_side(back)
    
    
    def flip_cube(self, forward=False):
        # if flipping forward, we set front to be top
        # top to be back, back to be bottom, and bottom
        # to be front, we must then invert the back and front

        # if flipping backward, we set front to be bottom
        # top to be front, back to be top, and bottom to be
        # back, we must then invert the top and bottom
        if forward:
            self.flip_forward()
            self.front = self.rotate_side(self.front)
            self.back = self.rotate_side(self.back)
        else:
            self.flip_backward()
            self.top = self.rotate_side(self.top)
            self.bottom = self.rotate_side(self.bottom)


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
        self.front = self.rotate_side(self.front)
        # swap the first row of the left/right side, and swap 
        # the last column of the left side with the first column of the right side
        self.top, self.bottom = self.swap_first_row(self.top, self.bottom)
        self.left, self.right = self.swap_first_last_col(self.left, self.right)
        
    def turn_back(self):
        # swap the last row of the left/right sides, and the first
        # row of the top/bottom sides
        self.turn_front

    
    def turn_left(self):
        # left become front, front becomes right, right becomes back, back becomes left
        # top gets rotated 90 degrees counter clockwise 
        # (3 6 9 -> 1 2 3) (2 5 8 -> 4 5 6) (1 4 7 -> 7 8 9)

        # turn the cube 90 degrees counter clockwise to face the
        # left side of the cube, now as the front, then turn_front
        self.rotate_cube()
        self.turn_front()

    
    def turn_right(self):
        # must make 3 90 degree rotations of the cube for the right
        # side to face front
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()
        self.right = self.rotate_side(self.right)
    
    def turn_top(self):
        self.flip_cube(forward=True)
        self.top = self.rotate_side(self.top)
    
    def turn_bottom(self):
        self.flip_cube()
        self.bottom = self.rotate_side(self.bottom)


x = State()
print(x)
top_row = x.front[0]
print()
x.turn_front()
bot_row = x.front[x.size - 1]
print(x)

#def move(s, a):
