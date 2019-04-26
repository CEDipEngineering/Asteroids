# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random
import time

pygame.init()
pygame.mixer.init()

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

pygame.mixer.music.load(path.join(snd_dir,'tgfcoder-FrozenJam-SeamlessLoop.ogg' ))
pygame.mixer.music.set_volume(0.4)
# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
def load_assets(img_dir,snd_dir):   
    assets= {}
    assets['player_img'] = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
    assets['asteroid_img'] = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
    assets['bullet_img'] = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
    assets['background_img'] = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
    assets['destroy_asteroid_snd'] = pygame.mixer.Sound(path.join(snd_dir,'expl6.wav')) 
    assets['player_hit_snd'] = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
    assets['shot_snd'] = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
    explosion_anim=[]
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir,filename)).convert()
        img = pygame.transform.scale(img,(32,32))
        img.set_colorkey(BLACK)
        explosion_anim.append(img)
    assets['explosion_anim'] = explosion_anim
    return assets

assets = load_assets(img_dir,snd_dir)
shot_sound = assets['shot_snd']
boom_sound = assets['player_hit_snd']
destroy_asteroid_sound = assets['destroy_asteroid_snd']
# Player
def randx():
    return random.randrange(0,WIDTH)
def randy():
    return random.randrange(-100,-40)
def randxspeed():
    return random.randrange(-2,2)
def randyspeed():
    return random.randrange(5,12)

class Player(pygame.sprite.Sprite):
    
    # Construtor
    def __init__(self,player_img):
        
        #Classe Pai
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de fundo
        self.image = player_img
        
        #Ajuste tamanho
        self.image = pygame.transform.scale(player_img,(50,38))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK)
        
        #Posicionamento
        self.rect = self.image.get_rect()
        
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.radius = 25
    
    def update(self):
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
class Mob(pygame.sprite.Sprite):
    
    
    def __init__(self,mob_img):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = mob_img
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = randx()
        self.rect.centery = randy()
        self.yspeed = randyspeed()
        self.xspeed = randxspeed()
        self.radius = int(self.rect.width * .85 / 2)
        
    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        
        if self.rect.bottom > HEIGHT:
            self.rect.centerx = randx()
            self.rect.centery = randy()
            self.xspeed = randxspeed()
            self.yspeed = randyspeed()
      
        
        
        
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x , y, bullet_img):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.yspeed = -10
    def update(self):
        self.rect.centery += self.yspeed
    
        if self.rect.bottom < 0:
            self.kill()
            
            
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, center, explosion_anim):
        
        pygame.sprite.Sprite.__init__(self)
        
        
        self.explosion_anim = explosion_anim
        
        self.frame = 0
        self.image = explosion_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        
        self.frame_ticks = 50
        
    def update(self):
        
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        
        
        if elapsed_ticks > self.frame_ticks:
            
            self.last_update = now
            
            self.frame+=1
            
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        
# Inicialização do Pygame.


# Tamanho da tela.


# Nome do jogo
pygame.display.set_caption("Asteroids")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = assets['background_img']
background_rect = background.get_rect()

#Cria um player do tipo Player
player = Player(assets['player_img'])

#Cria um mob do tipo Mob


#Cria um grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

mobs = pygame.sprite.Group()

bullets = pygame.sprite.Group()

for i in range(8):
    m = Mob(assets['asteroid_img'])
    mobs.add(m)
    all_sprites.add(m)
#time.sleep(2)
# Comando para evitar travamentos.
try:
    pygame.mixer.music.play(loops=-1)
    # Loop principal.
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                     
                    
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, assets['bullet_img'])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shot_sound.play()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
        all_sprites.update()
        asteroid_hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if asteroid_hits:
            boom_sound.play()
            time.sleep(1)
        
            running = False
       
        bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hits in bullet_hits:
            destroy_asteroid_sound.play()
            new_mob = Mob(assets['asteroid_img'])
            all_sprites.add(new_mob)
            mobs.add(new_mob)
            
            
            explosao = Explosion(hits.rect.center, assets['explosion_anim'])
            all_sprites.add(explosao)
        # A cada loop, redesenha o fundo e os sprites
        
        
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
