import pygame
import random

pygame.init() 

background = pygame.image.load("image/background.png")
bird = pygame.image.load("image/bird.png")
base = pygame.image.load("image/base.png")
gameover = pygame.image.load("image/gameover.png")
tube_down = pygame.image.load("image/tube.png")
tube_up = pygame.transform.flip(tube_down, False, True)

display = pygame.display.set_mode((288,512))
fps = 60
world_speed = 3
font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)


class tube_class:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75,150)
    def tube_draw(self):
        self.x -= world_speed
        display.blit(tube_down, (self.x, self.y+210))
        display.blit(tube_up, (self.x, self.y-210))
    def collision(self, bird, bird_x, bird_y):
        tolerance = 5
        bird_lato_r = bird_x + bird.get_width() - tolerance
        bird_lato_l = bird_x + tolerance
        tubes_lato_r = self.x + tube_down.get_width()
        tubes_lato_l = self.x
        bird_lato_up = bird_y + tolerance
        bird_lato_down = bird_y + bird.get_height() - tolerance
        tubes_lato_up = self.y + 110
        tubes_lato_down = self.y + 210
        if (bird_lato_r> tubes_lato_l and bird_lato_l < tubes_lato_r):
            if (bird_lato_up < tubes_lato_up or bird_lato_down > tubes_lato_down):
                game_over()
    def between_tubes(self, bird, bird_x):
        tolerance = 5
        bird_lato_r = bird_x + bird.get_width() - tolerance
        bird_lato_l = bird_x + tolerance
        tubes_lato_r = self.x + tube_down.get_width()
        tubes_lato_l = self.x
        if (bird_lato_r> tubes_lato_l and bird_lato_l < tubes_lato_r):
            return True 

def initialize():
    global bird_x, bird_y, bird_speed, base_x, tubes, points, between_tubes
    bird_x, bird_y = 60, 150
    bird_speed = 0
    base_x = 0
    tubes = []
    points = 0
    between_tubes = False
    tubes.append(tube_class())


def draw():
    display.blit(background, (0,0))
    display.blit(bird, (bird_x, bird_y))
    for t in tubes:
        t.tube_draw() 
    display.blit(base, (base_x,400))
    points_render = font.render(str(points), 1, (0,0,0))
    display.blit(points_render, (230,444))
    


def update():
    pygame.display.update()
    pygame.time.Clock().tick(fps)


def game_over():
    display.blit(gameover, (50,180))
    update()
    startover = False
    while not startover:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                initialize()
                startover = True
            if (event.type == pygame.QUIT):
                pygame.quit()


initialize()
while (True):
    #Avanzamento mondo
    base_x -= world_speed
    if (base_x < - 45):
        base_x = 0
    #Gravità
    bird_speed += 1
    bird_y += bird_speed
    #Comandi
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
            bird_speed = -10
        if (event.type == pygame.QUIT):
            pygame.quit()
    #Collisione tubi
    if (tubes[-1].x < 150): tubes.append(tube_class())
    for t in tubes:
        t.collision(bird, bird_x, bird_y)
    #Collisione con base
    if (bird_y > 380):
        game_over()
    #Aggiornamento punteggio
    if (not between_tubes):
        for t in tubes:
            if t.between_tubes(bird, bird_x):
                between_tubes = True
                break
    if (between_tubes):
        between_tubes = False
        for t in tubes:
            if t.between_tubes(bird, bird_x):
                between_tubes = True
                break
        if (not between_tubes):
            points += 1


    #Aggiornamento display
    draw()
    update()
