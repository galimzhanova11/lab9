import pygame
import random
import psycopg2




conn = psycopg2.connect(
	database="snake",
	user='postgres',
	password='rootroot',
	host='localhost',
	port= '5432'
)

cursor = conn.cursor()
conn.autocommit = True


# sql = '''CREATE TABLE players(
#    username VARCHAR(255) UNIQUE,
#    score INT
# )''';
# cursor.execute(sql)

def start_game():
    pygame.init()
    p = False
    n = 0

    FPS = 7
    a = False

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (153, 0, 204)
    PINK = (255, 102, 204)

    foodColor = BLUE
    food_color = [BLUE, PURPLE, PINK]

    score = 0
    level = 1

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    radius = 10
    body = [[30, 30], [0, 0], [0, 0]]

    block = 20
    dx, dy = block, 0

    class Wall():
        def __init__(self):
            self.body = []
            self.load_wall()
        def load_wall(self, level=1):
            with open(f'level{level}.txt', 'r') as f:
                wall_body = f.readlines()  
            for i, line in enumerate(wall_body):
                for j, value in enumerate(line):
                    if value == "#":
                        self.body.append([j, i]) 
        def draw(self): #function for drawing walls
            for x, y in self.body:
                pygame.draw.rect(screen, WHITE, (x * block, y * block, block, block))                     

    wall = Wall()
    # drawing grid
    def draw_grid():
        for i in range(0, WINDOW_WIDTH, block):
            for j in range(0, WINDOW_HEIGHT, block):
                pygame.draw.rect(screen, (100, 100, 100), (i, j, block, block), 1)

    def own_round(value, base=20):
        return base * round(value / 20) + 10

    # function for checking if food is on wall
    def food_on_wall(x, y):
        for i in wall.body:
            if i[0] * block + 10 == x and i[1] * block + 10 == y:
                return True
        return False       
    # function for checking if food is on snake`s body
    def food_on_body(x, y):
        for i in body:
            if i[0] == x and i[1] == y:
                return True
        return False    
    # function for checking if snake collides with wall
    def wall_collision():
        for i in wall.body:
            if i[0] * block + 10 == body[0][0] and i[1] * block + 10 == body[0][1]:
                return True
        return False               



    def set_random_position():
        x, y = own_round(random.randint(0 + 10, WINDOW_WIDTH - 10)), own_round(random.randint(0 + 10, WINDOW_HEIGHT - 10))
        while food_on_wall(x, y) or food_on_body(x, y):
            x, y = own_round(random.randint(0 + 10, WINDOW_WIDTH - 10)), own_round(random.randint(0 + 10, WINDOW_HEIGHT - 10))
        return x, y

    food_x, food_y = set_random_position()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dx = block
                    dy = 0
                if event.key == pygame.K_LEFT:
                    dx = -block
                    dy = 0
                if event.key == pygame.K_UP:
                    dx = 0
                    dy = -block
                if event.key == pygame.K_DOWN:
                    dx = 0
                    dy = block
                if event.key == pygame.K_SPACE:
                    p = True
                    n += 1 
                    print('i=', n)
                    # fps = FPS
                    # FPS = 0
                    # dx = 0
                    # dy = 0
                    sql = f'INSERT INTO players(username, score) values (%s, %s)'
                    insert_data = (user_name+str(n), score)
                    cursor.execute(sql, insert_data)
                    #print(user_name+str(n), score)
                if event.key == pygame.K_s:
                    p = False    

                

    # movement of snake
        if p == False:
            for i in range(len(body) - 1, 0, -1):
                body[i][0] = body[i - 1][0]
                body[i][1] = body[i - 1][1]
    
            body[0][0] += dx
            body[0][1] += dy
    # check if snake goes out of area
        if body[0][0] > 490:
            body[0][0] = 10
        if body[0][1] > 490:
            body[0][1] = 10   
        if body[0][0] < 10:
            body[0][0] = 490
        if body[0][1] < 10:
            body[0][1] = 490 
    # if food is pink then it will disappear in a few seconds
        if foodColor == PINK:
            time += 0.1
            #print(time)
            if time >= 5:
                food_x, food_y = set_random_position()
                c = random.randint(0, 2)
                foodColor = food_color[c]
                time = 0


    # Check for Food eating, if so, add one item to Snake body and increase score
        if food_x == body[0][0] and food_y == body[0][1]:
            # different scores for eating differen color food
            if foodColor == BLUE:  
                score += 1
            elif foodColor == PURPLE:
                score += 2
            elif foodColor == PINK:
                score += 3        
            if score >= 10:
                level = 2
                FPS = 10
                wall.load_wall(level=2)
            elif score >= 20:
                level = 3
                FPS = 13
                wall.load_wall(level=3)  
            
            body.append([0, 0])
            food_x, food_y = set_random_position() 
            c = random.randint(0, 2)
            foodColor = food_color[c] 
            if foodColor == PINK:
                time = 0  

    

        screen.fill(BLACK)

        draw_grid()
        wall.draw()
        

    # Draw food
        
        pygame.draw.circle(screen, foodColor, (food_x, food_y), radius)

    # Draw snake
        for i, (x, y) in enumerate(body):
            color = RED if i == 0 else GREEN
            pygame.draw.circle(screen, color, (x, y), radius)
    # show the score and level
        font = pygame.font.Font(None, 30)
        text = font.render(f'Score: {score}', True, RED)
        screen.blit(text, (20, 20))
        text2 = font.render(f'Level: {level}', True, BLUE)
        screen.blit(text2, (20, 40))
    # check for score. If it equal 30 then a person won
        if score >= 30:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 100)
            text = font.render('YOU WON!', True, RED)
            screen.blit(text, (85, 120))
    # check for collision with wall
        if wall_collision():  
            screen.fill(BLACK)
            font = pygame.font.Font(None, 100)
            text = font.render('YOU LOST!', True, RED)
            screen.blit(text, (80, 120))
            a = True
        for i in range(1, len(body)):
            if body[0][0] == body[i][0] and body[0][1] == body[i][1]:
                screen.fill(BLACK)
                font = pygame.font.Font(None, 100)
                text = font.render('YOU LOST!', True, RED)
                screen.blit(text, (80, 120))
                a = True     

        pygame.display.flip()
        if a:
            pygame.time.delay(3000)
            game_over = True

        clock.tick(FPS)

    pygame.quit()
    sql = f'INSERT INTO players(username, score) values (%s, %s)'
    insert_data = (user_name, score)
    cursor.execute(sql, insert_data)

user_name = input("username: ")

sql = f'select username, score from players where username = \'{user_name}\''
cursor.execute(sql)
score = cursor.fetchone()

if score != None:
    print("YOUR SCORE IS:", score[1])
    start_game()
else:
    print("STARTING GAME...")
    start_game()