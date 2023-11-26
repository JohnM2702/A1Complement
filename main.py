import pygame, os
from sys import exit 
from pygame_textinput import *

pygame.init()
FPS = 60
WIDTH,HEIGHT = 1024,768
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()


# Fonts
font = pygame.font.Font(os.path.join('fonts','InriaSans-Regular.ttf'),20)
font_italic = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),20)
name_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),30)


# Sounds
btn_sfx = pygame.mixer.Sound(os.path.join('audio','button_hover.wav'))


# Graphics
menu_bg = pygame.image.load(os.path.join('assets','menu_bg.png')).convert_alpha()
menu_bg_y = 0
menu_bg_height = menu_bg.get_height()
game_bg = pygame.image.load(os.path.join('assets','game_bg.png')).convert_alpha()

logo = pygame.image.load(os.path.join('assets','logo.png')).convert_alpha()
logo_rect = logo.get_rect(topleft = (280,46))

name_field = pygame.image.load(os.path.join('assets','name_field.png')).convert_alpha()
name_field_rect = name_field.get_rect(topleft = (292,325))

create_btn = pygame.image.load(os.path.join('assets','create.png')).convert_alpha()
create_btn_hover = pygame.image.load(os.path.join('assets','create_hover.png')).convert_alpha()
create_btn_rect = create_btn.get_rect(topleft = (355,417))

join_btn = pygame.image.load(os.path.join('assets','join.png')).convert_alpha()
join_btn_hover = pygame.image.load(os.path.join('assets','join_hover.png')).convert_alpha()
join_btn_rect = join_btn.get_rect(topleft = (355,525))

mechanics_btn = pygame.image.load(os.path.join('assets','mechanics.png')).convert_alpha()
mechanics_btn_hover = pygame.image.load(os.path.join('assets','mechanics_hover.png')).convert_alpha()
mechanics_btn_rect = mechanics_btn.get_rect(topleft = (355,633))

mechanics_bg = pygame.image.load(os.path.join('assets','mechanics_bg.png')).convert_alpha()
mechanics_bg_rect = mechanics_bg.get_rect(topleft=(26,35))


# Timers (custom events)
bg_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bg_timer,50)


def draw_mechanics():
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                update_menu_bg()
        
        SCREEN.fill(('#e1d4bb'))
        SCREEN.blit(menu_bg,(0,menu_bg_y))
        SCREEN.blit(menu_bg,(0,menu_bg_y-menu_bg_height+6))
        SCREEN.blit(mechanics_bg,mechanics_bg_rect)
        SCREEN.blit(logo,logo_rect)
        
        pygame.display.update()
        clock.tick(FPS)


# Scrolling background effect
def update_menu_bg():
    global menu_bg_y
    menu_bg_y += 1
    if menu_bg_y > menu_bg_height:
        menu_bg_y = 0  
    
    
def main_menu():
    manager = TextInputManager(validator=lambda input: len(input) <= 15)
    name_input = TextInputVisualizer(manager,name_font,cursor_blink_interval=500,cursor_width=2)
    field_clicked = False
    create_btn_hovered = False
    join_btn_hovered = False
    mechanics_btn_hovered = False
    
    while True:
        mechanics_clicked = False
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mechanics_clicked = True
            if event.type == bg_timer:
                update_menu_bg()

        # Background
        SCREEN.fill(('#e1d4bb'))
        SCREEN.blit(menu_bg,(0,menu_bg_y))
        SCREEN.blit(menu_bg,(0,menu_bg_y-menu_bg_height+6))
        
        # Logo
        SCREEN.blit(logo,logo_rect)
        
        # Name field
        name_label = font_italic.render('Name', True, (0,0,0))
        name_label_rect = name_label.get_rect(topleft=(325,301))
        SCREEN.blit(name_label, name_label_rect)
        SCREEN.blit(name_field, name_field_rect)
        SCREEN.blit(name_input.surface,(325,332))
        
        # Buttons
        SCREEN.blit(create_btn,create_btn_rect)
        SCREEN.blit(join_btn,join_btn_rect)
        SCREEN.blit(mechanics_btn,mechanics_btn_rect)
        
        mx, my = pygame.mouse.get_pos()
        lmb_clicked = pygame.mouse.get_pressed()[0]
        
        # Handle button hover & sfx
        if not field_clicked:
            if create_btn_rect.collidepoint(mx, my):
                if not create_btn_hovered:
                    btn_sfx.play()
                    create_btn_hovered = True
                    join_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(create_btn_hover, create_btn_rect)
            elif join_btn_rect.collidepoint(mx, my):
                if not join_btn_hovered:
                    btn_sfx.play()
                    join_btn_hovered = True
                    create_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(join_btn_hover, join_btn_rect)
            elif mechanics_btn_rect.collidepoint(mx, my):
                if not mechanics_btn_hovered:
                    btn_sfx.play()
                    mechanics_btn_hovered = True
                    create_btn_hovered = False
                    join_btn_hovered = False
                SCREEN.blit(mechanics_btn_hover, mechanics_btn_rect)
                if mechanics_clicked:
                    field_clicked = False
                    draw_mechanics()  # Display mechanics
            else: 
                mechanics_btn_hovered = False
                create_btn_hovered = False
                join_btn_hovered = False
        
        # Allow editing of player name if the name field was clicked
        if name_field_rect.collidepoint(mx,my) and lmb_clicked:
            field_clicked = True
        elif field_clicked and lmb_clicked and not name_field_rect.collidepoint(mx,my):
            field_clicked = False
        
        if field_clicked: name_input.update(events)
        
        pygame.display.update()
        clock.tick(FPS)
        
        
main_menu()