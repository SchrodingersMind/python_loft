import pygame
import random

class Background(object):
    def __init__(self, screen, tile_size, texts, list_numbers):
        self.screen = screen
        self.tile_size = tile_size
        self.texts = texts
        self.list_numbers = list_numbers
        
        self.block = pygame.Surface((tile_size - 4, tile_size - 4))
        self.block.fill((255 , 128, 0))
        pygame.draw.line(self.block, (0, 0, 0), (0, 0), (tile_size, 0), 2)
        pygame.draw.line(self.block, (0, 0, 0), (0, 0), (0, tile_size), 2)
        pygame.draw.line(self.block, (0, 0, 0), (tile_size - 2, 0), (tile_size - 2, tile_size - 2), 2)
        pygame.draw.line(self.block, (0, 0, 0), (0, tile_size - 2), (tile_size - 2, tile_size - 2), 2)
        
    def draw(self, numbers):
        begin = (70, 70)
        for i in range(4):
            for k in range(4):
                self.screen.blit(self.block, (begin[0] + i * self.tile_size, 
                                              begin[1] + k * self.tile_size))
                number = numbers[k][i]
                if number != '':
                    number_ind = self.list_numbers.index(str(number))
                    text = self.texts[number_ind]
                    width, height = text.get_size()
                    pos = (begin[0] + i * self.tile_size + (self.tile_size - width)  // 2,
                           begin[1] + k * self.tile_size + (self.tile_size - height) // 2)
                    self.screen.blit(text, pos)
        
        
numbers = [["" for k in range(4)] for i in range(4)]
points = 0
n_empty = 4 * 4

def parse_array(number_pos):    # If smth goes wrong, first check here
    global points, n_empty
    # by default shift on left side (paking/unpaking in "move" must/or not rotate
    
    prev = [-1, -1] # prev[0] - number in cell, prev[1] - location of this cell
    for k in range(4):
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
    #print(number_pos)
    # for second shift everything to left side
    shift_length = 0    # length to which we will shift our numbers
    for k in range(4):
        if number_pos[k] == "":
            shift_length += 1
            continue
        if shift_length == 0: continue
        number_pos[k-shift_length] = number_pos[k]
        number_pos[k] = ""
    return number_pos
    
def move(direction, numbers):
    prev_state = [numbers[i].copy() for i in range(4)]
    if direction == 0:
        for i in range(4):
            arr = [numbers[j][i] for j in range(4)]
            arr = parse_array(arr.copy())
            for j in range(4):
                numbers[j][i] = arr[j]
                
    elif direction == 1:
        for i in range(4):
            arr = [numbers[j][i] for j in range(4)]
            arr = arr[::-1]
            arr = parse_array(arr.copy())
            arr = arr[::-1]
            for j in range(4):
                numbers[j][i] = arr[j]
                
    elif direction == 2:
        for i in range(4):
            arr = [numbers[i][j] for j in range(4)]
            arr = arr[::-1]
            arr = parse_array(arr.copy())
            arr = arr[::-1]
            for j in range(4):
                numbers[i][j] = arr[j]
                
    elif direction == 3:
        for i in range(4):
            arr = numbers[i].copy()
            arr = parse_array(arr.copy())
            for j in range(4):
                numbers[i][j] = arr[j]
                
    return prev_state
                
def pop_up(numbers):
    global n_empty
    if n_empty == 0:
        return
    rand_pos = random.randint(0, 4*4 - 1)
    col = rand_pos % 4
    row = rand_pos // 4
    while numbers[row][col] != "": # not effective, must be changed
        rand_pos = random.randint(0, 4*4 - 1)
        col = rand_pos % 4
        row = rand_pos // 4 
    numbers[row][col] = "1"
    n_empty -= 1
    

def run_game(width, height, fps, numbers):
    
    pygame.init()
    
    font = pygame.font.SysFont("comicsansms", 32)
    texts = [font.render(str(pow(2, i)), True, (i * 14, 128 + i * 2 , 225 // (i + 1))) for i in range(16)]
    list_numbers = [str(pow(2, i)) for i in range(16)]
    tile_size = 70
    
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    done = False
    
    background = Background(screen, tile_size, texts, list_numbers)
    
    # Init secton
    pop_up(numbers)
    prev_numbers = numbers.copy()
    screen.fill((0, 128, 128))
    background.draw(numbers)
    pygame.display.flip()
    # Ebd of init section
    
    while not done:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        changed = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    done = True
                
                elif event.key == pygame.K_UP:
                    prev_numbers = move(0, numbers)
                    #print(prev_numbers)
                    #print(numbers)
                    changed = 1
                elif event.key == pygame.K_DOWN:
                    prev_numbers = move(1, numbers)
                    changed = 1
                elif event.key == pygame.K_RIGHT:
                    prev_numbers = move(2, numbers)
                    changed = 1
                elif event.key == pygame.K_LEFT:
                    prev_numbers = move(3, numbers)
                    changed = 1
                    
                if event.key == pygame.K_z:
                    if (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]):
                        numbers = [prev_numbers[i].copy() for i in range(4)]
                        changed = 2
                    
            

        if changed:
            if changed == 1:
                pop_up(numbers)
            screen.fill((0, 128, 128))
            background.draw(numbers)
            pygame.display.flip()
        clock.tick(fps)


width = 70 * 2 + 70 * 4     # Here we must use tile_size and begin variables
height = 70 * 2 + 70 * 4 
run_game(width, height, 30, numbers)
