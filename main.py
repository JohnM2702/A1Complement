import os
import pygame
from sys import exit 

pygame.init()

FPS = 60
WIDTH,HEIGHT = 1024,768
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()

font = pygame.font.Font(os.path.join('assets','InriaSans-Regular.ttf'),20)
font_italic = pygame.font.Font(os.path.join('assets','InriaSans-Italic.ttf'),20)


# Menu assets
menu_bg = pygame.image.load(os.path.join('assets','menu_bg.png')).convert()

logo = pygame.image.load(os.path.join('assets','logo.png')).convert_alpha()
logo_rect = logo.get_rect(topleft = (280,46))

name_field = pygame.image.load(os.path.join('assets','name_field.png')).convert_alpha()
name_field_rect = name_field.get_rect(topleft = (292,325))

create_game = pygame.image.load(os.path.join('assets','create_game.png')).convert_alpha()
create_game_rect = create_game.get_rect(topleft = (355,417))

join_game = pygame.image.load(os.path.join('assets','join_game.png')).convert_alpha()
join_game_rect = join_game.get_rect(topleft = (355,525))

mechanics = pygame.image.load(os.path.join('assets','mechanics.png')).convert_alpha()
mechanics_rect = mechanics.get_rect(topleft = (355,633))


def main_menu():
    WINDOW.blit(menu_bg,(0,0))
    WINDOW.blit(logo,logo_rect)
    
    name_label = font_italic.render('Name', True, (0,0,0))
    name_label_rect = name_label.get_rect(topleft=(325,301))
    WINDOW.blit(name_label, name_label_rect)
    
    WINDOW.blit(name_field, name_field_rect)
    WINDOW.blit(create_game,create_game_rect)
    WINDOW.blit(join_game,join_game_rect)
    WINDOW.blit(mechanics,mechanics_rect)
    
    pygame.display.update()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
                exit()
        
        main_menu()
        
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()