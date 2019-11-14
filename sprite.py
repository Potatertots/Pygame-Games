#pygame template - skeleton for new games
import pygame, sys
import random
import os

#set up asset folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assignment images')

#set framework stuff
WIDTH = 720
HEIGHT = 360
FPS = 60

#define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,'jump.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
    def update(self):
        self.rect.x += 2
        if self.rect.x >= WIDTH:
            self.rect.x = 0

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Title")
CLOCK = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#game loop
running = True

while running:
    #keep loop running at this speed
    CLOCK.tick(FPS)
    
    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    #update

    all_sprites.update()
    
    #draw/render
    SCREEN.fill(BLUE)
    all_sprites.draw(SCREEN)
    
    #after drawing everything, flip the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
    

