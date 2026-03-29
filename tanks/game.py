import pygame
from constants import *
import player

class Game():
    def __init__(self):
        self.game_window = None 
        self.allsprites = pygame.sprite.Group()

    
    def main_cycle(self):
        self.game_window = pygame.display.set_mode(WINDOW_SIZE) 
        time = pygame.time.Clock()
        game_on = True
        while game_on:
            #события
            events = pygame.event.get()
            for i in range(len(events)):
                if events[i].type == pygame.QUIT:
                    game_on = False 
            #логика


            #рисовка
            self.game_window.fill(BLACK)




            self.allsprites.update()
            self.game_window.fill(BLACK)
            self.allsprites.draw(self.game_window)
            pygame.display.update()
            time.tick(FPS)
        pygame.quit()
        
    def game_start(self):
        
        b = player.Player()
        self.allsprites.add(b)
        self.main_cycle()

        
        

        
a = Game()
a.game_start()




