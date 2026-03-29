import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(TANKUP_FILE)
        #изменить загрузку спрайта
        self.rect = self.image.get_rect()       
        self.rect.centerx = WINDOW_SIZE[0]/2
        self.rect.bottom = WINDOW_SIZE[0]/2
        
        self.TLEFT = pygame.image.load(TANKLEFT_FILE)
        self.TRIGHT = pygame.image.load(TANKRIGHT_FILE)
        self.TUP = pygame.image.load(TANKUP_FILE)
        self.TDOWN = pygame.image.load(TANKDOWN_FILE)
        
    def update(self):
        pressed_buttons = pygame.key.get_pressed()
        if pressed_buttons[pygame.K_a] and self.rect.left > 0:
            self.image = self.TLEFT
            self.rect.centerx -= PLAYER_SPEED
        elif pressed_buttons[pygame.K_d] and self.rect.right <= WINDOW_SIZE[0]:
            self.image = self.TRIGHT
            self.rect.centerx += PLAYER_SPEED
        elif pressed_buttons[pygame.K_w] and self.rect.top > 0 :
            self.image = self.TUP
            self.rect.centery -= PLAYER_SPEED
        elif pressed_buttons[pygame.K_s] and self.rect.bottom <= WINDOW_SIZE[1]:
            self.image = self.TDOWN
            self.rect.centery += PLAYER_SPEED