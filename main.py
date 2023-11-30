import pygame, os
from sys import exit 
from pygame_textinput import *
import subprocess
import threading
import queue
import time

# borrowing functions in server and clients
from server import Server, server_start, get_server
from client import client_start, client_init, get_client_name, client_message, get_server_size

pygame.init()
FPS = 60
WIDTH,HEIGHT = 1024,768
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()

# Colors
BLUE = '#537188'
BEIGE = '#E1D4BB'

# Fonts
font = pygame.font.Font(os.path.join('fonts','InriaSans-Regular.ttf'),20)
font_italic = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),20)
font_italic_big = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),40)
name_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),30)
answer_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),50)

# Player Name
manager = TextInputManager(validator=lambda input: len(input) <= 15)
name_input = TextInputVisualizer(manager,name_font,cursor_blink_interval=500,cursor_width=2)

# Sounds
btn_sfx = pygame.mixer.Sound(os.path.join('audio','button_hover.wav'))


# Graphics
menu_bg = pygame.image.load(os.path.join('assets','menu_bg.png')).convert_alpha()
bg_y = 0
bg_height = menu_bg.get_height()
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

loading0_icon = pygame.image.load(os.path.join('assets','loading_0.png')).convert_alpha()
loading1_icon = pygame.image.load(os.path.join('assets','loading_1.png')).convert_alpha()

mechanics_btn = pygame.image.load(os.path.join('assets','mechanics.png')).convert_alpha()
mechanics_btn_hover = pygame.image.load(os.path.join('assets','mechanics_hover.png')).convert_alpha()
mechanics_btn_rect = mechanics_btn.get_rect(topleft = (355,633))

mechanics_bg = pygame.image.load(os.path.join('assets','mechanics_bg.png')).convert_alpha()
mechanics_bg_rect = mechanics_bg.get_rect(topleft=(26,35))

number_two = pygame.image.load(os.path.join('assets','number_two.png')).convert_alpha()
number_two_hover = pygame.image.load(os.path.join('assets','number_two_hover.png')).convert_alpha()
number_two_rect = number_two.get_rect(topleft=(301,522))
number_four = pygame.image.load(os.path.join('assets','number_four.png')).convert_alpha()
number_four_hover = pygame.image.load(os.path.join('assets','number_four_hover.png')).convert_alpha()
number_four_rect = number_four.get_rect(topleft=(599,522))
number_three = pygame.image.load(os.path.join('assets','number_three.png')).convert_alpha()
number_three_hover = pygame.image.load(os.path.join('assets','number_three_hover.png')).convert_alpha()
number_three_rect = number_three.get_rect(topleft=(447,522))

loading_bg = pygame.image.load(os.path.join('assets','loading.png')).convert_alpha()
loading_bg_rect = loading_bg.get_rect(topleft=(269,384))

enter_btn = pygame.image.load(os.path.join('assets','enter.png')).convert_alpha()
enter_btn_hover = pygame.image.load(os.path.join('assets','enter_hover.png')).convert_alpha()
enter_btn_rect = enter_btn.get_rect(topleft=(401,570))

name_box = pygame.image.load(os.path.join('assets','name_box.png')).convert_alpha()
name_box_rect = name_box.get_rect(topleft=(355,487))

question_box = pygame.image.load(os.path.join('assets','question_box.png')).convert_alpha()
answer_box = pygame.image.load(os.path.join('assets','answer_box.png')).convert_alpha()
player_card = pygame.image.load(os.path.join('assets','player_card.png')).convert_alpha()
pcard_width = player_card.get_width()
pcard_height = player_card.get_height()


# Timers (custom events)
bg_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bg_timer,50)

# Game Global Variables specific to Client
# Reintegrate this to client sooon

def run_server():
    subprocess.run(['python','server.py'])

def run_client():
    subprocess.run(['python','client.py'])

def mechanics():
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                update_bg()
        
        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(mechanics_bg,mechanics_bg_rect)
        SCREEN.blit(logo,logo_rect)

        
        pygame.display.update()
        clock.tick(FPS)
        

def define_player_window():
    field_clicked = False
    create_btn_hovered = False
    join_btn_hovered = False
    mechanics_btn_hovered = False
    running = True
    while running:
        lmb_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                update_bg()
                
        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(loading_bg,loading_bg_rect)
        SCREEN.blit(logo,logo_rect)

        waiting_label = font_italic_big.render("Chose the Player Size",1,'Black')
        SCREEN.blit(waiting_label,(332,419))

        SCREEN.blit(number_two,number_two_rect)
        SCREEN.blit(number_three,number_three_rect)
        SCREEN.blit(number_four,number_four_rect)

        mx, my = pygame.mouse.get_pos()
        max_player_size = 4
        # Handle button hover & sfx
        if not field_clicked:
            if number_two_rect.collidepoint(mx, my):
                if not create_btn_hovered:
                    btn_sfx.play()
                    create_btn_hovered = True
                    join_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(number_two_hover, number_two_rect)
                if lmb_clicked:
                    max_player_size = 2
                    loading(max_player_size)
            elif number_three_rect.collidepoint(mx, my):
                if not join_btn_hovered:
                    btn_sfx.play()
                    join_btn_hovered = True
                    create_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(number_three_hover, number_three_rect)
                if lmb_clicked:
                    max_player_size = 3
                    loading(max_player_size)
            elif number_four_rect.collidepoint(mx, my):
                if not mechanics_btn_hovered:
                    btn_sfx.play()
                    mechanics_btn_hovered = True
                    create_btn_hovered = False
                    join_btn_hovered = False
                SCREEN.blit(number_four_hover, number_four_rect)
                if lmb_clicked:
                    max_player_size = 4
                    loading(max_player_size)
            else: 
                field_clicked = False
                mechanics_btn_hovered = False
                create_btn_hovered = False
                join_btn_hovered = False

        pygame.display.update()
        clock.tick(FPS)

def loading(max_players):
    loading_state = 0
    running = True
    loading_array = [0,0,0,0,0]
    refresh_count = 0

    # this is for setting up the shit
    server_start_thread = threading.Thread(target=server_start, args=(max_players,))
    server_start_thread.start()
    client_start()
    loading_state = 1
    while running:
        refresh_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                update_bg()

        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(loading_bg,loading_bg_rect)
        SCREEN.blit(logo,logo_rect)

        if loading_state == 1:
            a = 'Making the Game'
        elif loading_state == 0:
            a = 'Searching for Game'
        loading_label = "{}".format(a)
        waiting_label = font_italic_big.render(loading_label,1,'Black')
        SCREEN.blit(waiting_label,(347,419))

        player_count_value = get_server()

        if player_count_value == max_players:
            game_proper()

        player_count_text = "{}/{}".format(player_count_value, max_players)
        player_count = font_italic_big.render(player_count_text,1,'Black')
        SCREEN.blit(player_count,(477,492))

        
        for i in range(0,len(loading_array)):
            selected_icon = ""
            if loading_array[i] == 0:
                selected_icon = loading0_icon
            else:
                selected_icon = loading1_icon
            SCREEN.blit(selected_icon,(358+(67*i),576))

        if refresh_count % 50 == 0:
            if all(loading_array):
                for i in range(0,len(loading_array)):
                    loading_array[i] = 0
            else:
                for i in range(0,len(loading_array)):
                    if loading_array[i] == 0:
                        loading_array[i] = 1
                        break
            if refresh_count == 300:
                # change this to "when connected to client"
                loading_state = 1
                refresh_count = 0
        
        pygame.display.update()
        clock.tick(FPS)

def loading_client():
    loading_state = 0
    running = True
    loading_array = [0,0,0,0,0]
    refresh_count = 0

    client_start()
    loading_state = 1

    call_flag = 0
    player_count_value = 0
    while running:
        refresh_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                update_bg()

        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(loading_bg,loading_bg_rect)
        SCREEN.blit(logo,logo_rect)

        """
        while player_count_value == 0:
            client_message("><get_player_size")
            player_count_value = get_server_size()
            
            if player_count_value != 0:
                break
        """

        if loading_state == 1 and player_count_value != 0:
            a = 'Making the Game'

            player_count_text = "{}/{}".format(player_count_value[0], player_count_value[1])
            player_count = font_italic_big.render(player_count_text,1,'Black')
            SCREEN.blit(player_count,(477,492))

            if player_count_value[0] == player_count_value[1]:
                game_proper()
            
        else:
            a = 'Searching for Game'

        
        loading_label = "{}".format(a)
        waiting_label = font_italic_big.render(loading_label,1,'Black')
        SCREEN.blit(waiting_label,(347,419))

        # loading gui
        for i in range(0,len(loading_array)):
            selected_icon = ""
            if loading_array[i] == 0:
                selected_icon = loading0_icon
            else:
                selected_icon = loading1_icon
            SCREEN.blit(selected_icon,(358+(67*i),576))

        # refresh counting kek
        if refresh_count % 50 == 0:
            client_message("><get_player_size")
            player_count_value = get_server_size()
            if all(loading_array):
                for i in range(0,len(loading_array)):
                    loading_array[i] = 0
            else:
                for i in range(0,len(loading_array)):
                    if loading_array[i] == 0:
                        loading_array[i] = 1
                        break
            if refresh_count == 300:
                # change this to "when connected to client"
                loading_state = 1
                refresh_count = 0
        
        pygame.display.update()
        clock.tick(FPS)
        
def game_proper():
    # Temporary max input length
    # ideal: dynamically set when client can receive answers from server
    manager = TextInputManager(validator=lambda input: len(input) <= 15)
    answer_input = TextInputVisualizer(manager,answer_font,cursor_blink_interval=500,cursor_width=0)
    ongoing = True
    
    while ongoing:
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == bg_timer:
                update_bg()
            if event.type == pygame.KEYDOWN:    # Back to main menu (temp only!)
                if event.key == pygame.K_ESCAPE:
                    ongoing = False
        
        SCREEN.fill((BLUE))
        SCREEN.blit(game_bg,(0,bg_y))
        SCREEN.blit(game_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(question_box,(23,18))
        
        # Temporary hardcoded players
        # ideal: dynamically add when client can receive number of players from server
        SCREEN.blit(player_card,(23,494))
        p1_name = name_font.render(name_input.value,1,'Black')
        SCREEN.blit(p1_name,(35,562))
        p1_score = 0
        p1_score_surf = name_font.render(str(p1_score),1,'Black')
        SCREEN.blit(p1_score_surf,(35,602))
        
        x, y = 271, 283
        for i in range(3):
            SCREEN.blit(player_card,(x,494))
            p_name = name_font.render('Player',1,'Black')
            SCREEN.blit(p_name,(y,562))
            p_score_surf = name_font.render(str(x),1,'Black')
            SCREEN.blit(p_score_surf,(y,602))
            x += 248
            y += 248
            
        SCREEN.blit(answer_box,(23,669))
        answer_input_rect = answer_input.surface.get_rect(center=(WIDTH/2,715))
        SCREEN.blit(answer_input.surface,answer_input_rect)
        answer_input.update(events)
        
        pygame.display.update()
        clock.tick(FPS)
        

# Scrolling background effect
def update_bg():
    global bg_y
    bg_y += 1
    if bg_y > bg_height:
        bg_y = 0  
    
    
def main_menu():
    field_clicked = False
    create_btn_hovered = False
    join_btn_hovered = False
    mechanics_btn_hovered = False
    
    while True:
        lmb_clicked = False
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_clicked = True
            if event.type == bg_timer:
                update_bg()

        # Background
        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        
        # Logo
        SCREEN.blit(logo,logo_rect)
        
        # Name field
        name_label = font_italic.render('Hello there,', True, (0,0,0))
        name_label_rect = name_label.get_rect(topleft=(325,301))
        SCREEN.blit(name_label, name_label_rect)
        SCREEN.blit(name_field, name_field_rect)
        SCREEN.blit(name_input.surface,(325,332))
        
        # Buttons
        SCREEN.blit(create_btn,create_btn_rect)
        SCREEN.blit(join_btn,join_btn_rect)
        SCREEN.blit(mechanics_btn,mechanics_btn_rect)
        
        mx, my = pygame.mouse.get_pos()
        
        # Handle button hover & sfx
        if not field_clicked:
            if create_btn_rect.collidepoint(mx, my):
                if not create_btn_hovered:
                    btn_sfx.play()
                    create_btn_hovered = True
                    join_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(create_btn_hover, create_btn_rect)
                if lmb_clicked:
                    print("you just clicked create game")
                    #game_proper()
                    define_player_window()
                    
            elif join_btn_rect.collidepoint(mx, my):
                if not join_btn_hovered:
                    btn_sfx.play()
                    join_btn_hovered = True
                    create_btn_hovered = False
                    mechanics_btn_hovered = False
                SCREEN.blit(join_btn_hover, join_btn_rect)
                if lmb_clicked:
                    loading_client()
            elif mechanics_btn_rect.collidepoint(mx, my):
                if not mechanics_btn_hovered:
                    btn_sfx.play()
                    mechanics_btn_hovered = True
                    create_btn_hovered = False
                    join_btn_hovered = False
                SCREEN.blit(mechanics_btn_hover, mechanics_btn_rect)
                if lmb_clicked:
                    mechanics()  # Display mechanics
            else: 
                field_clicked = False
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

def player_name():
    field_clicked = False
    enter_btn_hovered = False
    
    while True:
        lmb_clicked = False
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_clicked = True
            if event.type == bg_timer:
                update_bg()

        # Background
        SCREEN.fill((BEIGE))
        SCREEN.blit(menu_bg,(0,bg_y))
        SCREEN.blit(menu_bg,(0,bg_y-bg_height+6))
        SCREEN.blit(loading_bg,loading_bg_rect)

        # Namebox and Button
        SCREEN.blit(name_box,name_box_rect)
        SCREEN.blit(enter_btn,enter_btn_rect)

        # Get the value of name_input
        player_name_value = name_input.value

        # Render player name on the screen
        player_name_surface = name_font.render(player_name_value, 1, 'Black')
        player_name_rect = player_name_surface.get_rect(center=(WIDTH / 2, 517))
        SCREEN.blit(player_name_surface, player_name_rect)

        # Label
        window_label = font_italic_big.render("Enter Your Name",1,'Black')
        SCREEN.blit(window_label,(365,419))
        
        # Logo
        SCREEN.blit(logo,logo_rect)

        mx, my = pygame.mouse.get_pos()
        
        # Handle button hover & sfx
        if not field_clicked:
            if enter_btn_rect.collidepoint(mx, my):
                if not enter_btn_hovered:
                    btn_sfx.play()
                    enter_btn_hovered = True
                SCREEN.blit(enter_btn_hover, enter_btn_rect)
                if lmb_clicked and player_name_value != '':
                    print(player_name_value,"has opened the game")
                    client_init(player_name = player_name_value)
                    main_menu()
                    #define_player_window()
                

        # Allow editing of player name if the name box was clicked
        if name_box_rect.collidepoint(mx, my) and lmb_clicked:
            field_clicked = True
        elif field_clicked and lmb_clicked and not player_name_rect.collidepoint(mx, my):
            print("not yeet")
            field_clicked = False
        if field_clicked: name_input.update(events)

        pygame.display.update()
        clock.tick(FPS)

player_name()       
#main_menu()
