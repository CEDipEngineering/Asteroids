# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')

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
        
    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        
        if self.rect.bottom > HEIGHT:
            self.rect.centerx = randx()
            self.rect.centery = randy()
            self.xspeed = randxspeed()
            self.yspeed = randyspeed()
        
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

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

mob = Mob()
mob2 = Mob()
mob3 = Mob()
mob4 = Mob()
mob5 = Mob()
mob6 = Mob()
mob7 = Mob()
mob8 = Mob()
#Cria um grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(mob)
all_sprites.add(mob2)
all_sprites.add(mob3)
all_sprites.add(mob4)
all_sprites.add(mob5)
all_sprites.add(mob6)
all_sprites.add(mob7)
all_sprites.add(mob8)

# Comando para evitar travamentos.
try:
    
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
        all_sprites.update()
        
        
        # A cada loop, redesenha o fundo e os sprites
        
        
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
