#!/usr/bin/env python3
import os
import time
import click
import random
from sys import exit, platform


points = 0
n_cell_x = 4
n_cell_y = 4
numbers = [["" for k in range(n_cell_x)] for i in range(n_cell_y)]
list_numbers = [str(pow(2, i)) for i in range(n_cell_x * n_cell_y)]
n_empty = n_cell_x * n_cell_y

arrow_up = b'\x1b[A'
arrow_down = b'\x1b[B'
arrow_right = b'\x1b[C'
arrow_left = b'\x1b[D'


def clearx(): #clear console
    if platform == 'linux':
        a = os.system('clear')
        del a
    elif platform == 'win32':
        a = os.system('cls')
        del a
    else:
        print('\n'*100)

def print_string(string, delay=0.1, color="33", tab=0):
    # print string like human
    colour = "\x1b[" +color+ "m"
    pre = " " * tab + colour
    for i in range(len(string)):
        print(pre + string[:i+1], end='\r')
        time.sleep(delay)
    print("\x1b[0m")
    
def print_square():
    global list_numbers
    length = 10 * 4
    begin = 20
    tab = " " * begin
    for i in range(length//2 + 1):
        if i % 5 == 0:
            print(tab + " " + "-" * length)
        else:
            string = tab 
            for k in range(0, length, 10):
                color_used = False
                string_tmp = "|"
                num_len = 0
                if i % 5 == 2:
                    num_len = len(numbers[i // 5][k // 10])
                spaces = (10 - num_len) // 2
                string_tmp += " " * spaces
                if i % 5 == 2:
                    number = numbers[i // 5][k // 10]
                    if number != "":
                        color_used = True
                        color = str(30 + (list_numbers.index(number)) % 7)    # I don't know why, but available only 6 colors
                        string_tmp += "\x1b[" + color + "m" + number + "\x1b[0m"
                string_tmp += " " * spaces
                if spaces * 2 + num_len + 1 != 10:
                    string_tmp += "  "
                    if color_used:
                        string_tmp = string_tmp[:19]
                    else: string_tmp = string_tmp[:10]
                string += string_tmp
            string += "|"
            print(string)
            
def parse_array(number_pos):    # If smth goes wrong, first check here
    global points, n_empty
    # by default shift on left side (paking/unpaking in "move" must/or not rotate
    length = len(number_pos) 
    
    # For first loop we only add matching cells
    prev = [-1, -1] # prev[0] - number in cell, prev[1] - location of this cell
    for k in range(length):
        if number_pos[k] == "":
            continue
        if prev[0] == number_pos[k]:
            #print(prev, number_pos, k)
            number_pos[prev[1]] = str(int(prev[0])*2)
            points += int(prev[0])
            n_empty += 1
            prev = [-1, -1]
            number_pos[k] = ""
            continue
        # if nothing matched
        prev = [number_pos[k], k]
    
    # For second, shift everything to left side
    shift_length = 0    # length to which we will shift our numbers
    for k in range(length):
        if number_pos[k] == "":
            shift_length += 1
            continue
        if shift_length == 0: continue
        number_pos[k-shift_length] = number_pos[k]
        number_pos[k] = ""
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
    while numbers[row][col] != "": # not effective, must be changed
        rand_pos = random.randint(0, n_cell_x*n_cell_y - 1)
        col = rand_pos % n_cell_x
        row = rand_pos // n_cell_x
    numbers[row][col] = "1"
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
    pop_up(numbers)
    
def print_game(numbers):
    # top line - our message with points
    clearx()
    #print_string("Points: " + str(points), delay=0, tab=columns//3)
    print_square()
    try:
        check_input(numbers)
    except:
        print("Smth goes wrong")
        exit()
    
pop_up(numbers)
while True:
    print_game(numbers)

