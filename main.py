import os
import pygame
from sys import exit 

pygame.init()

FPS = 60
WIDTH,HEIGHT = 1024,768
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()

test_font = pygame.font.SysFont(None, 20)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
                exit()
        
        WINDOW.fill((0,0,0))
        text = test_font.render('Test', True, (255,255,255))
        text_rect = text.get_rect(center = (WIDTH/2,HEIGHT/2))
        WINDOW.blit(text, text_rect)
        pygame.display.update()
        
        
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()