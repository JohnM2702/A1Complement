import pygame, os
from sys import exit 
pygame.init()

FPS = 60
WIDTH,HEIGHT = 1024,768
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()

font = pygame.font.Font(os.path.join('fonts','InriaSans-Regular.ttf'),20)
font_italic = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),20)


# Menu assets
menu_bg = pygame.image.load(os.path.join('assets','menu_bg.png')).convert()
game_bg = pygame.image.load(os.path.join('assets','game_bg.png')).convert()

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

mechanics_bg = pygame.image.load(os.path.join('assets','mechanics_bg.png')).convert_alpha()
mechanics_bg_rect = mechanics_bg.get_rect(topleft=(26,35))


def draw_mechanics():
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        WINDOW.blit(mechanics_bg,mechanics_bg_rect)
        WINDOW.blit(logo,logo_rect)
        
        pygame.display.update()
        clock.tick(FPS)
        
        
# click = False

def main_menu():
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    

        WINDOW.blit(menu_bg,(0,0))
        WINDOW.blit(logo,logo_rect)
        
        name_label = font_italic.render('Name', True, (0,0,0))
        name_label_rect = name_label.get_rect(topleft=(325,301))
        WINDOW.blit(name_label, name_label_rect)
        
        WINDOW.blit(name_field, name_field_rect)
        WINDOW.blit(create_game,create_game_rect)
        WINDOW.blit(join_game,join_game_rect)
        WINDOW.blit(mechanics,mechanics_rect)
        
        mx, my = pygame.mouse.get_pos()
        if mechanics_rect.collidepoint(mx,my):
            if click:
                draw_mechanics()
        
        pygame.display.update()
        clock.tick(FPS)
        
main_menu()