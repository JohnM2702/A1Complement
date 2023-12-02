from pygame_textinput import *
from network import Network
from game import Game
from sys import exit 
import pygame, os

pygame.init()
FPS = 60
WIDTH,HEIGHT = 1024,768
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Guessing Galore")
clock = pygame.time.Clock()
round_limit = 10000 # 10 seconds
network = Network()

# Colors
BLUE = '#537188'
BEIGE = '#E1D4BB'

# Fonts
font = pygame.font.Font(os.path.join('fonts','InriaSans-Regular.ttf'),20)
font_italic = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),20)
font_italic_big = pygame.font.Font(os.path.join('fonts','InriaSans-Italic.ttf'),40)
name_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),30)
answer_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),50)
game_info_font = pygame.font.Font(os.path.join('fonts','Lalezar-Regular.ttf'),35)

# Player Name
manager = TextInputManager(validator=lambda input: len(input) <= 15)
name_input = TextInputVisualizer(manager,name_font,cursor_blink_interval=750,cursor_width=2)

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
pcard_width, pcard_height = player_card.get_size()

game_box = pygame.image.load(os.path.join('assets','game_box.png')).convert_alpha()
gbox_width, gbox_height = game_box.get_size()
game_box_hover = pygame.image.load(os.path.join('assets','game_box_hover.png')).convert_alpha()
circle_waiting = pygame.image.load(os.path.join('assets','circle_waiting.png')).convert_alpha()
circle_full = pygame.image.load(os.path.join('assets','circle_full.png')).convert_alpha()


# Global Timers (custom events)
bg_timer = pygame.USEREVENT + 1
loading_timer = pygame.USEREVENT + 2
round_timer = pygame.USEREVENT + 3

pygame.time.set_timer(bg_timer,50)


def draw_bg(surface=None,rect=None,bg=menu_bg,draw_logo=True,color=BEIGE):
    SCREEN.fill((color))
    SCREEN.blit(bg,(0,bg_y))
    SCREEN.blit(bg,(0,bg_y-bg_height+6))
    if surface is not None and rect is not None:
        SCREEN.blit(surface,rect)
    if draw_logo:
        SCREEN.blit(logo,logo_rect)


def mechanics():
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                scroll_bg()
        draw_bg(mechanics_bg,mechanics_bg_rect)
        pygame.display.update()
        clock.tick(FPS)
        

def define_player_window():
    btn_rects = [[number_two,number_two_hover,number_two_rect,False,2],
                     [number_three,number_three_hover,number_three_rect,False,3],
                     [number_four,number_four_hover,number_four_rect,False,4]]
    running = True
    while running:
        lmb_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                scroll_bg()
                
        draw_bg(loading_bg,loading_bg_rect)

        waiting_label = font_italic_big.render("Chose the Player Size",1,'Black')
        SCREEN.blit(waiting_label,(332,419))

        mx, my = pygame.mouse.get_pos()
        
        for rect in btn_rects:
            SCREEN.blit(rect[0],rect[2])
            if rect[2].collidepoint(mx,my):
                if not rect[3]:
                    btn_sfx.play()
                    rect[3] = True 
                    for other_rect in btn_rects:
                        if other_rect is not rect:
                            other_rect[3] = False
                SCREEN.blit(rect[1],rect[2]) 
                if lmb_clicked:
                    running = False
                    create_game(rect[4])
            else: 
                rect[3] = False

        pygame.display.update()
        clock.tick(FPS)


def create_game(player_size):
    try:
        data = network.send_create(player_size,name_input.value)
    except Exception as e:
        print(f'Failed to create game: {e}')
        return

    if isinstance(data, str):
        # Handle case when max number of games have been reached
        # e.g. Display notice to player 
        pass
    else: loading(data)
    

def loading(game: Game):
    pygame.time.set_timer(loading_timer, 830)  # every 50 frames (50/60)
    waiting = True
    loading_array = [0, 0, 0, 0, 0]

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Handle this case later
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         running = False
            if event.type == bg_timer:
                scroll_bg()
            if event.type == loading_timer:
                if all(loading_array):
                    for i in range(0,len(loading_array)):
                        loading_array[i] = 0
                else:
                    for i in range(0,len(loading_array)):
                        if loading_array[i] == 0:
                            loading_array[i] = 1
                            break

        # Draw the screen
        draw_bg(loading_bg, loading_bg_rect)

        game_id = game.get_id()
        game_number = game_info_font.render(f'Game {game_id}', 1, 'black')
        SCREEN.blit(game_number, (449, 390))

        waiting_label = font_italic_big.render('Waiting for Players', 1, 'black')
        SCREEN.blit(waiting_label, (347, 444))

        player_count = game.get_player_count()
        player_size = game.get_player_size()
        player_count_text = f'{player_count}/{player_size}'
        player_count_render = font_italic_big.render(player_count_text, 1, 'Black')
        SCREEN.blit(player_count_render, (483, 500))

        for i in range(0, len(loading_array)):
            selected_icon = loading0_icon if loading_array[i] == 0 else loading1_icon
            SCREEN.blit(selected_icon, (358 + (67 * i), 576))

        pygame.display.update()
        clock.tick(FPS)

        try:
            data = network.wait_for_players()
        except:
            waiting = False
            print('[Waiting for Players]: Something went wrong.')
            return

        if not isinstance(data,Game):
            continue
        
        game = data
        waiting = game.get_player_count() < game.get_player_size()

    game_proper(game)


def fetch_games():
    try:
        return network.send("fetch games")
    except Exception as e:
        print(f'Failed to fetch games: {e}')
        return None


def view_games():
    games = fetch_games()
    running = True
    
    while running:
        lmb_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == bg_timer:
                scroll_bg()
        
        draw_bg(mechanics_bg,mechanics_bg_rect)
        games = fetch_games()

        if isinstance(games, dict) and len(games) > 0:
            game_box_rects = []
            count, x, y = 1, 0, 340
            circle = circle_waiting

            for game_id, game in games.items():
                game_number = game_info_font.render(f'Game {game_id}',1,'black')
                p_count = game.get_player_count()
                p_size = game.get_player_size()
                player_count_text = f'{p_count}/{p_size}'
                player_count_surf = game_info_font.render(player_count_text,1,'Black')
                
                if p_count == p_size: circle = circle_full
                
                if count % 2 == 0: x = 586
                else: x = 121

                game_box_rect = pygame.Rect(x,y,gbox_width,gbox_height)
                circle_coords = (x+22,y+28)
                gnumber_coords = (x+64,y+20)
                pcount_coords = (x+237,y+20)
                game_box_rects.append([game_box_rect,circle_coords,gnumber_coords,pcount_coords,game_id])
                
                count += 1
                if count == 2: y += 132
                elif count == 4: y += 132

            mx, my = pygame.mouse.get_pos()
            
            # Handle button hover, sfx, and click
            for rect in game_box_rects:
                if rect[0].collidepoint(mx,my): 
                    SCREEN.blit(game_box_hover,rect[0])
                    if lmb_clicked:
                        join_game(rect[4])
                else: 
                    SCREEN.blit(game_box,rect[0])
                SCREEN.blit(circle,rect[1])
                SCREEN.blit(game_number,rect[2])
                SCREEN.blit(player_count_surf,rect[3])
                
        pygame.display.update()
        clock.tick(FPS)


def join_game(game_id:int):
    try:
        data = network.send_join(game_id,name_input.value)
    except Exception as e: 
        print(f'Failed to join game: {e}')
        return

    if isinstance(data, str):
        # Handle case when game is full 
        # i.e. (other client joined just milliseconds before you)
        # e.g. Display notice to player 
        pass
    else: 
        if data.has_started(): game_proper(data)
        else: loading(data)

    
def game_proper(game:Game):
    pygame.time.set_timer(round_timer,round_limit)

    # Temporary max input length
    # ideal: dynamically set when client can receive answers from server
    manager = None
    answer_input = TextInputVisualizer(manager,answer_font,cursor_blink_interval=500,cursor_width=0)
    ongoing = True
    
    while ongoing:
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == bg_timer:
                scroll_bg()
            if event.type == pygame.KEYDOWN:    # Back to main menu (temp only!)
                if event.key == pygame.K_ESCAPE:
                    ongoing = False
            if event.type == round_timer:
                # Time's up
                pass
        
        draw_game(game)
            
        
        answer_input_rect = answer_input.surface.get_rect(center=(WIDTH/2,715))
        SCREEN.blit(answer_input.surface,answer_input_rect)
        answer_input.update(events)
        
        pygame.display.update()
        clock.tick(FPS)
        

def draw_game(game:Game):
    draw_bg(bg=game_bg,draw_logo=False,color=BLUE)
    SCREEN.blit(question_box,(23,18))
    players = game.get_players()
    card_x, card_y = 23, 494
    name_x, name_y = 35, 562
    score_x, score_y = 35, 602
    for id, data in players.items():
        name = name_font.render(data['name'],1,'black')
        score = name_font.render(str(data['score']),1,'black')
        SCREEN.blit(player_card,(card_x,card_y))
        SCREEN.blit(name,(name_x,name_y))
        SCREEN.blit(score,(score_x,score_y))
        card_x += 248
        name_x += 248
        score_x += 248
    SCREEN.blit(answer_box,(23,669))


# Scrolling background effect
def scroll_bg():
    global bg_y
    bg_y += 1
    if bg_y > bg_height:
        bg_y = 0  


def main_menu():
    field_clicked = False
    name_input.cursor_visible = False
    btn_rects = [[create_btn,create_btn_hover,create_btn_rect,False],
                     [join_btn,join_btn_hover,join_btn_rect,False],
                     [mechanics_btn,mechanics_btn_hover,mechanics_btn_rect,False]]
    
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
                scroll_bg()

        draw_bg()
        
        # Name field
        name_label = font_italic.render('Hello there,', True, (0,0,0))
        name_label_rect = name_label.get_rect(topleft=(325,301))
        SCREEN.blit(name_label, name_label_rect)
        SCREEN.blit(name_field, name_field_rect)
        SCREEN.blit(name_input.surface,(325,332))
        
        mx, my = pygame.mouse.get_pos()
        
        # Buttons
        for rect in btn_rects: 
            SCREEN.blit(rect[0],rect[2])
            if name_input.value != '':
                if rect[2].collidepoint(mx,my):
                    if rect[3] is False:
                        btn_sfx.play()
                        rect[3] = True
                        for other_rect in btn_rects:
                            if other_rect is not rect:
                                other_rect[3] = False 
                    SCREEN.blit(rect[1],rect[2])
                    if lmb_clicked:
                        if rect[0] is create_btn:
                            define_player_window()
                        elif rect[0] is join_btn:
                            view_games()
                        else: 
                            mechanics()
                else: 
                    rect[3] = False
                        
        # Allow editing of player name if the name field was clicked
        if name_field_rect.collidepoint(mx,my) and lmb_clicked:
            field_clicked = True
        elif field_clicked and lmb_clicked and not name_field_rect.collidepoint(mx,my):
            field_clicked = False
            name_input.cursor_visible = False
        if field_clicked: name_input.update(events)
        
        pygame.display.update()
        clock.tick(FPS)
        

def player_name():
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
                scroll_bg()

        draw_bg(loading_bg,loading_bg_rect)

        # Label
        window_label = font_italic_big.render("Enter Your Name",1,'Black')
        SCREEN.blit(window_label,(365,419))
        
        # Namebox and Button
        SCREEN.blit(name_box,name_box_rect)
        SCREEN.blit(enter_btn,enter_btn_rect)

        # Get the value of name_input
        player_name_value = name_input.value

        # Render player name on the screen
        player_name_surf = name_input.surface
        player_name_rect = player_name_surf.get_rect(center=(WIDTH/2,517))
        SCREEN.blit(name_input.surface,player_name_rect)
        name_input.update(events)

        mx, my = pygame.mouse.get_pos()
        
        # Handle button hover & sfx
        if player_name_value != '':
            if enter_btn_rect.collidepoint(mx, my):
                if not enter_btn_hovered:
                    btn_sfx.play()
                    enter_btn_hovered = True
                SCREEN.blit(enter_btn_hover, enter_btn_rect)
                if lmb_clicked:
                    print(player_name_value,"has opened the game")
                    while True:
                        main_menu()
            else: 
                enter_btn_hovered = False
                
        pygame.display.update()
        clock.tick(FPS)


player_name()
