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
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
shot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
destroy_asteroid_sound = pygame.mixer.Sound(path.join(snd_dir,'expl6.wav')) 
# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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
    def __init__(self):
        
        #Classe Pai
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de fundo
        player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
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
    
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        mob_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
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
    
    def __init__(self, x , y):
        
        pygame.sprite.Sprite.__init__(self)
        
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
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
            
# Inicialização do Pygame.


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

#Cria um player do tipo Player
player = Player()

#Cria um mob do tipo Mob


#Cria um grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

mobs = pygame.sprite.Group()

bullets = pygame.sprite.Group()

for i in range(8):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

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
                    bullet = Bullet(player.rect.centerx, player.rect.top)
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
            new_mob = Mob()
            all_sprites.add(new_mob)
            mobs.add(new_mob)
        # A cada loop, redesenha o fundo e os sprites
        
        
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
