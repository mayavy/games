
import random
import keyboard as k
import os
import time


# allowed e:end, up,down, left,right, o:O, x:X


class Line:
    """ Each line printed on console is object of this class.
state: defines purpose of the line
char: character type where required  """

    def __init__(self, char='_', state=''):

        self.lst = ['|']+list(' '*46)+['|']

        if state == 'blank':
            self.lst = [' '] + list(char*46)

        if state == 'vert':
            self.lst = ['|'] + list(' '*14) + ['||'] + \
                list(' '*14) + ['||'] + list(' '*14) + ['|']
        if state == 'horz':
            self.lst = [' '] + list('='*46)

        self.out = self.lst

    def __str__(self):
        st = ''.join(self.out)
        return st

    def check_cursor(self, cursor_loc, count):
        """ prints bouncing cursor """
        y, x = cursor_loc
        if y == count:
            char_list = ['_', '-']
            rand = random.randint(0, 9)
            char = char_list[rand % 2]

            self.out[(15*x)+6] = char
            self.out[(15*x)+7] = char
            self.out[(15*x)+8] = char
            self.out[(15*x)+9] = char
        return self


class Segment:
    """ line-segment connecting two point coordinates of individual type of markers"""

    def __init__(self, y1, x1, y2, x2):
        self.y1x1 = (y1, x1)
        self.y2x2 = (y2, x2)
        self.slope = ((y2-y1), (x2-x1))

    def straight_with(self, segment):
        """check if two segements are forming a straightline to declare winner"""
        return self.slope == segment.slope and (self.y2x2 == segment.y1x1)


def modify_o(row, col):
    """ takes row:[Line(), ..] -> modifies line objects to renders
    the o-marker """
    line0, line1, line2, line3, line4, line5, line6 = row
    line1.out[15*col+4: 15*col+12] = '  ____  '
    line2.out[15*col+4: 15*col+12] = '/      \\'
    line3.out[15*col+4: 15*col+12] = '|      |'
    line4.out[15*col+4: 15*col+12] = '\\ ____ /'


def modify_x(row, col):
    """ takes row:[Line(), ..] -> modifies line objects to renders
    the x-marker """
    line0, line1, line2, line3, line4, line5, line6 = row
    line1.out[15*col+4: 15*col+10] = ' \  / '
    line2.out[15*col+4: 15*col+10] = '  \/  '
    line3.out[15*col+4: 15*col+10] = '  /\  '
    line4.out[15*col+4: 15*col+10] = ' /  \ '


def welcome(atstart):
    if atstart:
        os.system('cls')  # clear screen

        print(Line(state='blank'))
        for i in range(7):
            print(Line())

        print("|            welcome to Tic-Tac-Toe            |")
        print(Line())
        print(Line())
        print('|use up,down,left and right arrow keys to move |')
        print("|      press button 'O' to enter O-marker      |")
        print("|      press button 'X' to enter X-marker      |")
        print("|   press button 'E' to exit during gameplay   |")
        print(Line())
        print("|        Now press button 'Enter' play         |")

        for i in range(7):
            print(Line())

        print(Line(char='-', state='blank'))

        k.wait('enter')


class GameLoop:
    def __init__(self):

        row0 = []  # three rows in game
        row1 = []
        row2 = []

        cursor_loc = (0, 0)  # current location of cursor
        y, x = cursor_loc
        marked_dict = {}  # dictonary with already marked coordiantes:marks
        prev_len = 0  # one turn behind lenght of marked_dict

        x_segment = []  # list of all segments formed by connecting x-markers
        o_segment = []  # list of all segments formed by connecting o-markers

        atstart = 1  # controller to excute only at start
        previous = 'none'  # marker in previous turn
        run = 1  # keeps the game loop running

        while run:  # game loop

            welcome(atstart)

            horz0 = Line(state='horz')  # 1st === line
            horz1 = Line(state='horz')  # 2nd === line
            last = Line(char='-', state='blank')  # last --- line

            if k.is_pressed('e'):  # press 'e' to exit game
                break

            os.system('cls')  # clear screen

            print(Line(state='blank'))  # top ___ line

            for i in range(7):
                if atstart:
                    row0 += [Line(state='vert')]
                print(row0[i])

            # print 1st === line
            print(horz0.check_cursor(cursor_loc, count=0))

            for i in range(7):
                if atstart:
                    row1 += [Line(state='vert')]
                print(row1[i])

            # print 2nd === line
            print(horz1.check_cursor(cursor_loc, count=1))

            for i in range(7):
                if atstart:
                    row2 += [Line(state='vert')]
                print(row2[i])

            # print last --- line
            print(last.check_cursor(cursor_loc, count=2))

            if len(marked_dict) > prev_len:
                for coord, m in marked_dict.items():
                    # at each turn store new segment in respective list
                    if m == 'x' and marked_dict[cursor_loc] == 'x' and cursor_loc != coord:
                        loc0 = coord
                        loc1 = cursor_loc
                        if coord > cursor_loc:
                            loc1 = coord
                            loc0 = cursor_loc
                        x_segment += [Segment(*loc0, *loc1)]

                    if m == 'o' and marked_dict[cursor_loc] == 'o' and cursor_loc != coord:
                        loc0 = coord
                        loc1 = cursor_loc
                        if coord > cursor_loc:
                            loc1 = coord
                            loc0 = cursor_loc
                        o_segment += [Segment(*loc0, *loc1)]

                segmentxo = {'o': o_segment, 'x': x_segment}
                for mark, each in segmentxo.items():
                    for segment in each:
                        for newsegment in each:
                            if newsegment != segment and segment.straight_with(newsegment):
                                print(f'\n {mark.upper()} won !!')
                                run = 0

                            elif len(marked_dict) == 9 and run:  # game draw :)
                                print(f'\n Game Drawn !!')
                                run = 0

            # x_ = list([(seg.y1x1, seg.y2x2, seg.slope) for seg in x_segment])
            # o_ = list([(seg.y1x1, seg.y2x2, seg.slope) for seg in o_segment])
            # print(f'{x_}: x, {o_}: o')

            prev_len = len(marked_dict)

            # marking the markers into row lists
            rown = [row0, row1, row2]
            if cursor_loc not in marked_dict:

                if k.is_pressed('x') and previous != 'x':
                    modify_x(rown[y], x)
                    marked_dict[cursor_loc] = 'x'
                    previous = 'x'

                if k.is_pressed('o') and previous != 'o':
                    modify_o(rown[y], x)
                    marked_dict[cursor_loc] = 'o'
                    previous = 'o'

            atstart = 0

        # cursor control, move left,right,up,down, cyclically

            if k.is_pressed('down'):
                y += 1
            if k.is_pressed('up'):
                y -= 1

            if k.is_pressed('right'):
                x += 1

            if k.is_pressed('left'):
                x -= 1

            if y > 2:
                y = 0
            if x > 2:
                x = 0

            if y < 0:
                y = 2
            if x < 0:
                x = 2

            cursor_loc = (y, x)

            # time.sleep(0.1)


launch = GameLoop()
