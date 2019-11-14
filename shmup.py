#pygame template - skeleton for new games
import pygame, sys
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'zero hour stuff')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup")
CLOCK = pygame.time.Clock()

#define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#load all game graphics and sound
background = pygame.image.load(path.join(img_dir,'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,'playerShip2_blue.png')).convert()
player_mini_img = pygame.transform.scale(player_img,(25,25))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir,'laserBlue16.png')).convert()


meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png','meteorBrown_big3.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png']
for i in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,i)).convert())


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir,'shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir,'gun.png')).convert()

    
shoot_sound = pygame.mixer.Sound(path.join(img_dir, 'pew.wav'))
meteor_sounds = []
m_snd_list = ['expl3.wav', 'expl6.wav']
for i in m_snd_list:
    meteor_sounds.append(pygame.mixer.Sound(path.join(img_dir,i)))
#load music file
pygame.mixer.music.set_volume(0.4)




#text writing function
font_name = pygame.font.match_font('courier')
def draw_text(surf, text, size, x, y, colour):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text,True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

#defining player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 20
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        self.power = 1
        self.power_time = pygame.time.get_ticks()

        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        #timeout for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            if self.power >=2:
                bullet2 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        

#defining Mob objects
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.radius = int(self.rect.width * 0.85 /2)
        self.health = self.radius * 2
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now-  self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + self.rect.height or self.rect.left < -self.rect.width or self.rect.right > WIDTH + self.rect.width:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
            self.speedx = random.randrange(-3,3)


#defining Bullet objects
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.damage = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#defining explosion sprites
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame+=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#powerup class
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if  moves off bottom of screen
        if self.rect.top > HEIGHT:
            self.kill()
    

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)

def show_go_screen():
    SCREEN.blit(background,background_rect)
    draw_text(SCREEN, "SHMUP!", 64, WIDTH/2, HEIGHT/4, WHITE)
    draw_text(SCREEN, "Arrow keys move, space to fire", 22, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(SCREEN, "Press any key to begin", 18, WIDTH/2, HEIGHT * 3/4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    
        

#groups n stuff
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    newmob()



score = 0
#pygame.mixer.music.play(loops = -1)

#game loop
running = True
game_over = True

while running:
    if game_over:
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
        game_over = False
    #keep loop running at this speed
    CLOCK.tick(FPS)
    
    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        
    
    #update
    all_sprites.update()

    #check to see if mob hits player
    hits = pygame.sprite.spritecollide(player,mobs,True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        
        newmob()
        
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            player.hide()

    #check if player is alive
    if player.lives == 0 and not death_explosion.alive():
        game_over = True


    #check to see if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullets,True, True)
    for hit in hits:
        score += 60 - hit.radius
        random.choice(meteor_sounds).play()
        newmob()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pup = Pow(hit.rect.center)
            all_sprites.add(pup)
            powerups.add(pup)


    #check to see if player hits powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    
    #draw/render
    SCREEN.fill(BLACK)
    SCREEN.blit(background,background_rect)
    
    all_sprites.draw(SCREEN)

    draw_text(SCREEN, str(score), 18, WIDTH/2, 10, WHITE)
    
    draw_shield_bar(SCREEN,5,5,player.shield)
    draw_text(SCREEN,str(player.shield), 14,15,5, WHITE)

    draw_lives(SCREEN, WIDTH-100,5,player.lives,player_mini_img)
    
    #after drawing everything, flip the screen
    pygame.display.flip()


pygame.quit()
sys.exit()
    
