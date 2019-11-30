import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((300, 400))
head_color = (128, 0, 200)
body_color = (0, 128, 255)
done = False
clock = pygame.time.Clock()
direction = "right"
yh = 30
xh = 50
xb = [40]
yb = [30]
chery = (randint(2, 30-3)*10, randint(2, 40-3)*10)
points = 0
sections = 1
brick_10 = pygame.image.load("brick_10.png")
brick_20 = pygame.image.load("brick_20.png")
chery_music = pygame.mixer.Sound("match4.wav")

def default(): # used to resset to initial values
    global yh, xh, xb, yb, chery, sections, direction, points
    yh, xh = 30, 20
    xb, yb = [10], [30]
    chery = (randint(2, 30-3)*10, randint(2, 40-3)*10)
    sections = 1
    direction = "right"
    points = 0


while not done:
    clock.tick(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction == "up" or direction == "down": break 
                direction = "up"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction == "up" or direction == "down": break
                direction = "down"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction == "right" or direction == "left": break
                direction = "right"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction == "right" or direction == "left": break
                direction = "left"
            elif event.key == pygame.K_r:
                default()
    
    # change snake position
    for i in range(sections-1):
        xb[i], yb[i] = xb[i+1], yb[i+1]
    xb[-1], yb[-1] = xh, yh
    if direction == "up": yh -= 10
    elif direction == "down": yh += 10
    elif direction == "left": xh -= 10
    elif direction == "right": xh += 10
    
    #draw screen, chery, body and head
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(chery[0], chery[1], 10, 10)) 
    for i in range(sections):
        pygame.draw.rect(screen, body_color, pygame.Rect(xb[i], yb[i], 10, 10))
        if xh == xb[i] and yh == yb[i]: #eat myself
            default()
            break
    pygame.draw.rect(screen, head_color, pygame.Rect(xh, yh, 10, 10))
    
    # draw border
    for i in range(20):
        screen.blit(brick_20, (0, i*20))
        screen.blit(brick_20, (280, i*20))
    for i in range(13):
        screen.blit(brick_20, (i*20+20, 0))
        screen.blit(brick_20, (i*20+20, 380))
    
    #check for border corruption
    if xh == 10 or xh == 280 or yh == 10 or yh == 380:
        default()
    
    # true if chery eated
    if xh == chery[0] and yh == chery[1]:
        chery_music.play()
        chery = (randint(2, 30-3)*10, randint(2, 40-3)*10)  # "-1" to avoid appearing chery out of border
        points +=100
        sections +=1
        xb.append(xh)
        yb.append(yh)
        print(points)
        
        
    pygame.display.flip()
