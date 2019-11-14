#pygame template - skeleton for new games
import pygame, sys
import random
import math
from os import path


#variables
WIDTH = 600
HEIGHT = 700
FPS = 60

#define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroidz")
CLOCK = pygame.time.Clock()

#define text stuff
font_name = pygame.font.match_font('courier')

#load images
img_dir = path.dirname(__file__)

background = pygame.image.load(path.join(img_dir,'stars.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir,'playerShip3_orange.png')).convert()
player_img.set_colorkey(BLACK)
player_mini = pygame.transform.scale(player_img, (25,19))
player_mini.set_colorkey(BLACK)

kipling = pygame.image.load(path.join(img_dir,'kipling.png')).convert()
kipling.set_colorkey(BLACK)
kipling = pygame.transform.scale(kipling,(100,200))

shield_img = pygame.image.load(path.join(img_dir,'shield1.png')).convert()
shield_img = pygame.transform.scale(shield_img,(100,66))
shield_img.set_colorkey(BLACK)
shield_rect = shield_img.get_rect()

bullet_imgs = {}
bullet_imgs['reg'] = pygame.image.load(path.join(img_dir,'laserBlue01.png')).convert()
bullet_imgs['pup'] = pygame.image.load(path.join(img_dir,'laserGreen11.png')).convert()
bullet_imgs['double'] = pygame.image.load(path.join(img_dir,'laserRed01.png')).convert()

meteor_imgs = {}
meteor_imgs['small'] = pygame.image.load(path.join(img_dir, 'm1.png')).convert()
meteor_imgs['med'] = pygame.image.load(path.join(img_dir, 'm2.png')).convert()
meteor_imgs['lg'] = pygame.image.load(path.join(img_dir, 'm3.png')).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

powerup_images = {}
powerup_images['gun'] = pygame.image.load(path.join(img_dir,'gun.png')).convert()
powerup_images['shield'] = pygame.image.load(path.join(img_dir,'shield.png')).convert()
powerup_images['double'] = pygame.image.load(path.join(img_dir,'double.png')).convert()

#load sounds
shoot_sound = pygame.mixer.Sound(path.join(img_dir, 'pew.wav'))

expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(img_dir, snd)))

pygame.mixer.music.load(path.join(img_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

#miscellaneous variables
score = 0
level = 0

#initialize player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 20
        self.image_orig = pygame.transform.scale(player_img,(50,38))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.rangle = 0
        self.angle = 0
        self.damage = 25

        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        self.type = 'reg'


    def update(self):
        #key movement
        self.speedx = 0
        self.speedy = 0
        self.damage = 25 + 5*level
        
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0 and self.rect.top > -100:
            self.rect.top = 0
        if self.rect.bottom >HEIGHT:
            self.rect.bottom = HEIGHT

        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        #rotation
        mousex, mousey = pygame.mouse.get_pos()
        if (self.rect.centerx - mousex) != 0:
            self.rangle = math.atan((self.rect.centery - mousey)/(self.rect.centerx - mousex))

        if mousex < self.rect.centerx:
            self.angle = math.degrees(self.rangle) % 360 - 90
        if mousex >= self.rect.centerx:
            self.angle = math.degrees(self.rangle) % 360 - 270
            
        new_image = pygame.transform.rotate(self.image_orig,-self.angle)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        #unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT / 2

        #powerups
        now = pygame.time.get_ticks()
        if self.type != 'reg' and now - self.power_time >= 6000:
            self.type = 'reg'


    def shoot(self):
        now = pygame.time.get_ticks()
        if self.type == 'pup':
            self.shoot_delay = 100
        else:
            self.shoot_delay = 200

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.type, self.angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            if self.type == 'double':
                self.last_shot = now
                bullet = Bullet(self.rect.right, self.rect.centery, self.type, self.angle)
                bullet2 = Bullet(self.rect.left, self.rect.centery, self.type, self.angle)
                all_sprites.add(bullet, bullet2)
                bullets.add(bullet, bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, -200)
        
#defining bullet objects
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,btype,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_imgs[btype]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10 * math.sin(math.radians(angle-90))
        self.speedx = 10 * math.cos(math.radians(angle-90))
        self.damage = 10

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.centerx > WIDTH or self.rect.centerx < 0:
            self.kill()

#defining mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = meteor_imgs[random.choice(['small','med','lg'])]
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/2)
        self.rect.y = random.randrange(-80,HEIGHT + 80)
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.rect.x = random.randrange(WIDTH)
        else:
            self.rect.x = random.choice([-40,WIDTH+40])
        self.speedx = random.randrange(1,4)
        if self.rect.x > WIDTH/2:
            self.speedx = -self.speedx
        self.speedy = random.randrange(1,4)
        if self.rect.y > HEIGHT/2:
            self.speedy = - self.speedy
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

        self.health = self.radius * 5


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.y = random.randrange(-80,HEIGHT + 80)
            if self.rect.y < 0 or self.rect.y > HEIGHT:
                self.rect.x = random.randrange(WIDTH)
            else:
                self.rect.x = random.choice([0,WIDTH])
            self.speedx = random.randrange(1,4)
            if self.rect.x > WIDTH/2:
                self.speedx = -self.speedx
            self.speedy = random.randrange(1,4)
            if self.rect.y > HEIGHT/2:
                self.speedy = - self.speedy
        

#explosion class
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
        if now- self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#powerup class
class Pow(pygame.sprite.Sprite):
    def __init__(self, center, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun', 'double'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

#boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = kipling
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = -50
        self.speedx = 0
        self.speedy = 2
        self.init_health = level * 100
        self.health = self.init_health

    def update(self):
        if self.rect.y == 100 and self.rect.x == 100:
            self.speedx = 2
            self.speedy = 0
        if self.rect.x == 350:
            self.speedx = 0
            self.speedy = 2
        if self.rect.y == 350:
            self.speedy = 0
            self.speedx = -2
        if self.rect.x == 100 and self.rect.y == 350:
            self.speedy = -2
            self.speedx = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy
            

def draw_text(surf, text, size, x, y, colour):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text,True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)
    

def show_go_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "SHMUP!", 64, WIDTH/2, HEIGHT/4, WHITE)
    draw_text(SCREEN, "Arrow keys move, mouse to rotate, space to fire", 18, WIDTH/2, HEIGHT/2, WHITE)
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

def newmob():
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

def draw_bar(surf,x,y,pct,xsize,ysize):
    if pct < 0:
        pct = 0
    BARLENGTH = xsize
    BARHEIGHT = ysize
    fill = pct/100 * BARLENGTH
    outline_rect = pygame.Rect(x,y,BARLENGTH,BARHEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BARHEIGHT)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
    pygame.draw.rect(surf,GREEN,fill_rect)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


#setting up groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bosses = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(4):
    newmob()


pygame.mixer.music.play(loops = -1)


#game loop
running = True
game_over = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        score = 0
        level = 0
        player.shield = 100
        player.lives = 3
        while len(mobs.sprites()) > 4:
            mobs.sprites()[0].kill()
    
    #keep loop running at this speed
    CLOCK.tick(FPS)
    
    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    #update
    all_sprites.update()


    #check for mob hits player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        player.shield -= hit.radius * 2
        newmob()
        if player.shield < 0:
            player.hide()
            player.lives -= 1
            player.shield = 100
        if player.lives <= 0:
            game_over = True

    #check if bullet hits mob
    shots = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for shot in shots:
        shot.health -= player.damage
        if shot.health <= 0:
            shot.kill()
            newmob()
            if random.random() > 0.5:
                powup = Pow(shot.rect.center, shot.speedx, shot.speedy)
                all_sprites.add(powup)
                powerups.add(powup)
        expl = Explosion(shot.rect.center, 'lg')
        all_sprites.add(expl)
        score += shot.radius*3
        if score >= 1000:
            level += 1
            score = 0
            for i in range(2):
                newmob()
            if level % 3 == 0:
                b = Boss()
                bosses.add(b)
                all_sprites.add(b)
        random.choice(expl_sounds).play()
        

    #check if player picks up powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.type = 'pup'
            player.power_time = pygame.time.get_ticks()
        if hit.type == 'double':
            player.type = 'double'
            player.power_time = pygame.time.get_ticks()

    #check if bullet hits boss
    hits = pygame.sprite.groupcollide(bosses, bullets, False, True)
    for hit in hits:
        hit.health -= player.damage
        if hit.health <= 0:
            hit.kill()
            expl = Explosion(hit.rect.center, 'lg')
        score += 100

    #check if player hits boss
    hits = pygame.sprite.spritecollide(player, bosses, False)
    for hit in hits:
        player.shield -= 30
        if player.shield <=0:
            player.hide()
            player.lives -= 1
            player.shield = 100
        if player.lives <= 0:
            game_over = True
            

    
    #draw/render
    SCREEN.fill(BLACK)
    SCREEN.blit(background,background_rect)

    shield_rect.center = player.rect.center
    shield_img.set_alpha(player.shield/100 * 200)
    SCREEN.blit(shield_img,shield_rect)
    
    all_sprites.draw(SCREEN)
    mobs.draw(SCREEN)
    
    draw_text(SCREEN, str(score), 24, 30, 20, WHITE)
    draw_text(SCREEN, 'Level: ' + str(level), 18, WIDTH-70, 20, WHITE)
    draw_bar(SCREEN, 5, 5, player.shield, 100, 10)
    draw_lives(SCREEN, 10, HEIGHT-20, player.lives, player_mini)



    for mob in mobs.sprites():
        draw_bar(SCREEN, mob.rect.left, mob.rect.bottom + 5, 100 * mob.health/(mob.radius * 5), mob.radius*2, 3)

    for boss in bosses.sprites():
        draw_bar(SCREEN, boss.rect.left, boss.rect.bottom + 5, 100 * boss.health/boss.init_health, 100, 3)

    #after drawing everything, flip the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
    
