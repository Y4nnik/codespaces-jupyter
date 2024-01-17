import pygame
import sys
from pygame.math import Vector2 # import the vector2 class
import random

class FRUIT:
   def __init__(self):
       self.x = random.randint(0, cell_number-1) # create a random x position
       self.y = random.randint(0, cell_number-1) # create a random y position
       self.pos = Vector2(self.x, self.y) # create a vector2 object with the x and y position
   def draw_fruit(self):
       fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)    
       screen.blit(apple, fruit_rect) # draw the fruit at the fruit_rect position
   def randomize(self):
       self.x = random.randint(0, cell_number-1) # create a random x position
       self.y = random.randint(0, cell_number-1) # create a random y position
       self.pos = Vector2(self.x, self.y) # create a vector2 object with the x and y position
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]  
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    
    def update_head_graphics(self): 
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self): 
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if not self.direction == Vector2(0,0):
            if self.new_block == True:
                body_copy = self.body[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1] # create a copy of the body without the last element
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]  
        self.direction = Vector2(0,0)
        
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        global score
        score = len(self.snake.body) - 3
        self.snake.reset()
        global pygame_state
        pygame_state = "game_over"
    
    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3) # create a string with the score
        score_surface = game_font.render(score_text, True, (56,74,12)) # create a surface with the text and color (True is for anti-aliasing)
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
pygame.init()
cell_size = 40
cell_number = 20
pygame_state = "start"
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()
running = True
apple = pygame.image.load('graphics/apple.png').convert_alpha()
sn = pygame.image.load('snake.png').convert_alpha()
sn = pygame.transform.scale(sn, (200, 200))
gosn = pygame.image.load('gameoversnake.png').convert_alpha()
gosn = pygame.transform.scale(gosn, (200, 200))
game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 35) # create a font object
score = 0
main_game = MAIN()

def draw_start_menu():
    screen.fill((175,215,70))
    main_game.draw_grass()
    font = pygame.font.SysFont('arial', 40)
    titlefont = pygame.font.SysFont('arial', 80)
    start_rect = pygame.Rect(cell_number*cell_size/2-200, cell_number*cell_size/2-200, 400, 400)
    pygame.draw.rect(screen,(87,65,47), start_rect, 0, 10)
    start_button = font.render('Press "Space" to Start', True, (255, 255, 255))
    title = titlefont.render('Pysnake', True, (255, 255, 255))
    snake_rect = pygame.Rect(start_rect.centerx-100, start_rect.centery-100, 180, 180)
    screen.blit(title, (cell_number*cell_size/2 - title.get_width()/2, cell_number*cell_size/2 - 180))
    screen.blit(start_button, (cell_number*cell_size/2 - start_button.get_width()/2, cell_number*cell_size/2+100))
    screen.blit(sn, snake_rect) # draw the fruit at the fruit_rect position
    pygame.display.update()

def draw_game_over_menu():
    screen.fill((175,215,70))
    main_game.draw_grass()
    font = pygame.font.SysFont('arial', 40)
    score_screen = font.render('Your Score: ' + str(score), True, (255, 255, 255))
    titlefont = pygame.font.SysFont('arial', 60)
    start_rect = pygame.Rect(cell_number*cell_size/2-200, cell_number*cell_size/2-200, 400, 400)
    pygame.draw.rect(screen,(87,65,47), start_rect, 0, 10)
    start_button = font.render('Press "Space" to Restart', True, (255, 255, 255))
    title = titlefont.render('Game Over', True, (255, 255, 255))
    snake_rect = pygame.Rect(start_rect.centerx-100, start_rect.centery-50, 180, 180)
    screen.blit(title, (cell_number*cell_size/2 - title.get_width()/2, cell_number*cell_size/2 - 180))
    screen.blit(start_button, (cell_number*cell_size/2 - start_button.get_width()/2, cell_number*cell_size/2+150))
    screen.blit(gosn, snake_rect) # draw the fruit at the fruit_rect position
    screen.blit(score_screen, (cell_number*cell_size/2 - score_screen.get_width()/2, cell_number*cell_size/2 - 100))
    pygame.display.update()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
      if event.type == SCREEN_UPDATE and pygame_state == "game":
            main_game.update()
      if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1 and main_game.snake.direction != Vector2(0,0):
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0) 
            if event.key == pygame.K_SPACE and (pygame_state == "start" or pygame_state == "game_over"):
                pygame_state = "game"   
                main_game.snake.direction = Vector2(0,0)

   if pygame_state == "start":
        draw_start_menu()
   if pygame_state == "game":
        screen.fill((175,215,70)) # fill the screen with green 
        main_game.draw_elements()
        pygame.display.update()
   if pygame_state == "game_over":
        draw_game_over_menu()
   clock.tick(120)  # limits FPS to 60
