from operator import length_hint
import pygame
import time
import random
 
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)
 
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
 
WIDTH = 600
HEIGHT = 400
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')




 
clock = pygame.time.Clock()
 
sn = 10
speed = 5
level = 1


 
font_s = pygame.font.SysFont("consolas", 25)
score_f = pygame.font.SysFont("consolas", 20)
 
 
def Your_score(score):
    score = score_f.render("Your Score: " + str(score), True, BLUE)
    SCREEN.blit(score, [0, 0])

def Your_level(lev):
    lev = score_f.render("Your Level: " + str(lev), True, BLUE)
    SCREEN.blit(lev, [0, 15])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(SCREEN, BLACK, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_s.render(msg, True, color)
    SCREEN.blit(mesg, [WIDTH / 14, HEIGHT / 3])
 
 
def gameLoop():
    
    level_up = False
    game_over = False
    game_close = False

    
 
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    length = 1
    

 
    foodx = round(random.randrange(50, WIDTH - sn-50) / 10.0) * 10.0
    foody = round(random.randrange(50, HEIGHT - sn-50) / 10.0) * 10.0
    size = 10
    timer = 5
    
 
    while not game_over:

        

        while level_up == True:

            SCREEN.fill(WHITE)
            message("Level up. Press C to continue", BLUE)
            Your_score(length - 1)
            global level
            Your_level(level)
            pygame.display.update()
            
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        level_up = False
                        global speed 
                        speed = speed + 3
                        
                        gameLoop()

            

        while game_close == True:

            SCREEN.fill(WHITE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            Your_score(length - 1)
            Your_level(level)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            gameLoop()

 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.USEREVENT: 
                timer -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -sn
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = sn
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -sn
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = sn
                    x1_change = 0

        

            

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, GREEN, [foodx, foody, size, size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        
        if (length%5 == 0):
            level_up = True
            level = level + 1
 
        our_snake(sn, snake_List)
        Your_score(length - 1)
        Your_level(level)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            size = random.randint(5, 13)
            foodx = round(random.randrange(50, WIDTH - sn - 50) / 10.0) * 10.0
            foody = round(random.randrange(50, HEIGHT - sn - 50) / 10.0) * 10.0
            length += 1
        
        if (timer < 0):
                    size = random.randint(5, 13)
                    foodx = round(random.randrange(50, WIDTH - sn - 50) / 10.0) * 10.0
                    foody = round(random.randrange(50, HEIGHT - sn - 50) / 10.0) * 10.0
                    timer = 5
        
        clock.tick(speed)

    pygame.quit()
    quit()
 
 
gameLoop()