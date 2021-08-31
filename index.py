import pygame, sys
import os
import random
from pygame.display import flip

def draw_floor():
    screen.blit(floor_surface,(floor_x_position,HEIGHT-floor_surface.get_height()))
    screen.blit(floor_surface,(floor_x_position+WIDTH,HEIGHT-floor_surface.get_height()))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (WIDTH+pipe_surface.get_width(),random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (WIDTH+pipe_surface.get_width(),random_pipe_pos - 150))
    # top_pipe = pygame.transform.flip(top_pipe,False,True)
    return bottom_pipe,top_pipe
    
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe ,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False

def game_over():
    gameOver = pygame.image.load(os.path.join('Assets','sprites','gameover.png'))
    screen.blit(gameOver,(WIDTH/2-gameOver.get_width()/2,HEIGHT/2-gameOver.get_height()))

def game_start():
    gameStart = pygame.image.load(os.path.join('Assets','sprites','message.png'))
    screen.blit(gameStart,(WIDTH/2-gameStart.get_width()/2,HEIGHT/2-gameStart.get_height()))

pygame.init()
WIDTH = 288
HEIGHT = 512
screen = pygame.display.set_mode((WIDTH,HEIGHT))
Clock = pygame.time.Clock()

#game variables
gravity = 0.25
bird_movement = 0
game_active = True
game_start = False
game_end = False

bg_surface = pygame.image.load(os.path.join('Assets','sprites','background-day.png')).convert()

floor_surface = pygame.image.load(os.path.join('Assets','sprites','base.png')).convert()
floor_x_position = 0

bird_surface = pygame.image.load(os.path.join('Assets','sprites','yellowbird-midflap.png')).convert()
bird_rect = bird_surface.get_rect(center=(50,HEIGHT/2))

pipe_surface = pygame.image.load(os.path.join('Assets','sprites','pipe-green.png'))
pipe_list = []
pipe_height = [200,250,300,350,400]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6
        
        if event.type == SPAWNPIPE:
            pipe_list.extend (create_pipe())

    screen.blit(bg_surface,(0,0))
    # intro()
    if game_active and game_start == False and game_end == False:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        if check_collision(pipe_list) == False:
            game_active = False
            game_end = True

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
    
    if game_active == False and game_end == True:
        game_over()
    


    draw_floor()
    floor_x_position -= 1
    if floor_x_position <= -WIDTH:
        floor_x_position = 0

    pygame.display.update()
    Clock.tick(60)

