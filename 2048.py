#!/usr/bin/env python3
import os
import time
import click
import random
from sys import exit, platform

points = 0
n_cell_x = 4
n_cell_y = 4
numbers = [[0 for k in range(n_cell_x)] for i in range(n_cell_y)]
list_numbers = [pow(2, i) for i in range(n_cell_x * n_cell_y)]
n_empty = n_cell_x * n_cell_y

# Read more at http://ascii-table.com/ansi-escape-sequences.php
FG_COLOR = '\x1b[30m'
BG_COLOR = '\x1b[47m'

arrow_up = b'\x1b[A'
arrow_down = b'\x1b[B'
arrow_right = b'\x1b[C'
arrow_left = b'\x1b[D'

def clearx():
    """ Clear console """
    if platform == 'linux':
        a = os.system('clear')
        del a
    elif platform == 'win32':
        a = os.system('cls')
        del a
    else:
        print('\n'*100)


def print_string(string, delay=0.1, color="33", tab=0):
    # print string like human (char by char)
    colour = "\x1b[" +color+ "m"
    pre = " " * tab + colour
    for i in range(len(string)):
        print(pre + string[:i+1], end='\r')
        time.sleep(delay)
    print("\x1b[0m")
    

def print_square():
    def generate_empty_table():
        """ Create grid without numbers """
        row_len = table_left_margin + 1 + (1+cell_inner_width)*n_cell_x
        count_rows = table_up_margin + 1 + (1+cell_inner_height)*n_cell_y

        table = [[""] for y in range(table_up_margin)] 
        for y in range(count_rows-table_up_margin):
            now_row = [" "] * table_left_margin
            if y % (cell_inner_height+1) == 0:
                now_row += ["+"] + (["-"] * cell_inner_width + ["+"]) * n_cell_x
            else:
                now_row += ["|"] + ([" "] * cell_inner_width + ["|"]) * n_cell_x
            table.append(now_row)

        return table


    def fill_empty_by_numbers(table):
        """ Put numbers into cells """
        for y in range(n_cell_y):
            for x in range(n_cell_x):
                number = numbers[y][x]
                if not(number):
                    continue
                
                    # Find place for number
                num_row = (table_up_margin + 1 + cell_inner_height//2) \
                        + (cell_inner_height+1)*y
                start_pos = (table_left_margin + 1) \
                        + (cell_inner_width+1)*x
                end_pos = start_pos + cell_inner_width

                    # Put number in center of cell and add colors
                    # I don't know why, but available only 6 colors
                color = str(30 + (list_numbers.index(number)) % 7)    
                strip = list(str(number).center(cell_inner_width, " "))
                
                table[num_row][start_pos:end_pos] = strip
                table[num_row][start_pos] = f"\x1b[{color}m" + table[num_row][start_pos]
                table[num_row][end_pos-1] += FG_COLOR

                
    def output_table(table):
        """Print grid"""
        print(FG_COLOR)
        for row in table:
            for symbol in row:
                print(symbol, end="")
            print()


    cell_inner_width = 5
    cell_inner_height = 0
    table_left_margin = 20
    table_up_margin = 3  
    
    t = generate_empty_table()
    fill_empty_by_numbers(t)
    output_table(t)
            
def parse_array(number_pos):    # If smth goes wrong, first check here
    global points, n_empty
    # by default shift on left side (paking/unpaking in "move" must/or not rotate
    length = len(number_pos) 
    
    # For first loop we only add matching cells
    prev = [-1, -1] # prev[0] - number in cell, prev[1] - location of this cell
    for k in range(length):
        if number_pos[k] == 0:
            continue
        if prev[0] == number_pos[k]:
            #print(prev, number_pos, k)
            number_pos[prev[1]] = prev[0]*2
            points += prev[0]
            n_empty += 1
            prev = [-1, -1]
            number_pos[k] = 0
            continue
        # if nothing matched
        prev = [number_pos[k], k]
    
    # For second, shift everything to left side
    shift_length = 0    # length to which we will shift our numbers
    for k in range(length):
        if number_pos[k] == 0:
            shift_length += 1
            continue
        if shift_length == 0: continue
        number_pos[k-shift_length] = number_pos[k]
        number_pos[k] = 0
    return number_pos
    
def move(direction, numbers):
    if direction == 0:
        for i in range(n_cell_x):
            arr = [numbers[j][i] for j in range(n_cell_y)]
            arr = parse_array(arr.copy())
            for j in range(n_cell_y):
                numbers[j][i] = arr[j]
                
    elif direction == 1:
        for i in range(n_cell_x):
            arr = [numbers[j][i] for j in range(n_cell_y)]
            arr = arr[::-1]
            arr = parse_array(arr.copy())
            arr = arr[::-1]
            for j in range(n_cell_y):
                numbers[j][i] = arr[j]
                
    elif direction == 2:
        for i in range(n_cell_y):
            arr = [numbers[i][j] for j in range(n_cell_x)]
            arr = arr[::-1]
            arr = parse_array(arr.copy())
            arr = arr[::-1]
            for j in range(n_cell_x):
                numbers[i][j] = arr[j]
                
    elif direction == 3:
        for i in range(n_cell_y):
            arr = numbers[i].copy()
            arr = parse_array(arr.copy())
            for j in range(n_cell_x):
                numbers[i][j] = arr[j]
            
                
def pop_up(numbers):
    global n_empty
    if n_empty == 0: return
    rand_pos = random.randint(0, n_cell_x*n_cell_y - 1)
    col = rand_pos % n_cell_x
    row = rand_pos // n_cell_x
    while numbers[row][col]: # not effective, must be changed
        rand_pos = random.randint(0, n_cell_x*n_cell_y - 1)
        col = rand_pos % n_cell_x
        row = rand_pos // n_cell_x
    numbers[row][col] = 1
    n_empty -= 1

def check_input(numbers):
    k = click.getchar().encode()
    if k == arrow_up:
        move(0, numbers)
    elif k == arrow_down:
        move(1, numbers)
    elif k == arrow_right:
        move(2, numbers)
    elif k == arrow_left:
        move(3, numbers)
    else:
        # Do nothing, if user click on other button
        return
    pop_up(numbers)
    
def print_game(numbers):
    # top line - our message with points
    clearx()
    #print_string("Points: " + str(points), delay=0, tab=columns//3)
    print_square()
    try:
        check_input(numbers)
    except KeyboardInterrupt:
        print("Cleaning.......")
        print("\x1b[0m")
        clearx()
        exit()

  
# Set defaults colors for fore- and back-ground
print(BG_COLOR)   
pop_up(numbers)
while True:
    print_game(numbers)

