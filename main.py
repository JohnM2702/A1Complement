from network import Network, net_test
from asset_loader import load_images
from pygame_textinput import *
from threading import Thread
from game import Game
from sys import exit
import pygame, os
import random

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
inria_20 = pygame.font.Font(os.path.join('assets','fonts','InriaSans-Regular.ttf'),20)
inria_50 = pygame.font.Font(os.path.join('assets','fonts','InriaSans-Regular.ttf'),50)
inria_40 = pygame.font.Font(os.path.join('assets','fonts','InriaSans-Regular.ttf'),40)
inria_50.align = pygame.FONT_CENTER
inria_italic_20 = pygame.font.Font(os.path.join('assets','fonts','InriaSans-Italic.ttf'),20)
inria_italic_40 = pygame.font.Font(os.path.join('assets','fonts','InriaSans-Italic.ttf'),40)
lalezar_30 = pygame.font.Font(os.path.join('assets','fonts','Lalezar-Regular.ttf'),30)
lalezar_35 = pygame.font.Font(os.path.join('assets','fonts','Lalezar-Regular.ttf'),35)
lalezar_50 = pygame.font.Font(os.path.join('assets','fonts','Lalezar-Regular.ttf'),50)

# Player Name
manager = TextInputManager(validator=lambda input: len(input) <= 15)
name_input = TextInputVisualizer(manager,lalezar_30,cursor_blink_interval=750,cursor_width=2)

# Sounds
btn_sfx_click = pygame.mixer.Sound(os.path.join('assets','sfx','button_click.wav'))
btn_sfx_hover = pygame.mixer.Sound(os.path.join('assets','sfx','button_hover.ogg'))
sfx_error = pygame.mixer.Sound(os.path.join('assets','sfx','error.ogg'))
bgm_sound = pygame.mixer.Sound(os.path.join('assets','bgm','bgm.mp3'))

type_1 = pygame.mixer.Sound(os.path.join('assets','sfx','type_1.mp3'))
type_2 = pygame.mixer.Sound(os.path.join('assets','sfx','type_2.mp3'))
type_3 = pygame.mixer.Sound(os.path.join('assets','sfx','type_3.mp3'))
type_4 = pygame.mixer.Sound(os.path.join('assets','sfx','type_4.mp3'))

screen_transition = pygame.mixer.Sound(os.path.join('assets','sfx','screen_transition.mp3'))
correct = pygame.mixer.Sound(os.path.join('assets','sfx','correct.mp3'))
victory = pygame.mixer.Sound(os.path.join('assets','sfx','victory.mp3'))
notifcation = pygame.mixer.Sound(os.path.join('assets','sfx','notification.mp3'))

# Images
images: dict[str,pygame.Surface] = load_images()

logo_rect = images['logo'].get_rect(topleft = (280,46))
name_field_rect = images['name_field'].get_rect(topleft = (292,325))
create_btn_rect = images['create_btn'].get_rect(topleft = (355,417))
join_btn_rect = images['join_btn'].get_rect(topleft = (355,525))
mechanics_btn_rect = images['mechanics_btn'].get_rect(topleft = (355,633))
mechanics_bg_rect = images['mechanics_bg'].get_rect(topleft=(26,35))
number_two_rect = images['number_two'].get_rect(topleft=(301,522))
number_four_rect = images['number_four'].get_rect(topleft=(599,522))
number_three_rect = images['number_three'].get_rect(topleft=(447,522))
loading_bg_rect = images['loading_bg'].get_rect(topleft=(269,384))
enter_btn_rect = images['enter_btn'].get_rect(topleft=(401,570))
name_box_rect = images['name_box'].get_rect(topleft=(355,487))

exit_game_btn_rect = images['exit_game_btn'].get_rect(topleft=(491,481))

congrats_label_rect = images['congrats_label'].get_rect(topleft=(294,194))
win_label_rect = images['congrats_label_2'].get_rect(topleft=(485,367))

pcard_width, pcard_height = images['player_card'].get_size()
gbox_width, gbox_height = images['game_box'].get_size()
qbox_width, qbox_height = images['question_box'].get_size()
bg_height = images['menu_bg'].get_height()
bg_y = 0

# Global Timers (custom events)
bg_timer = pygame.USEREVENT + 1
loading_timer = pygame.USEREVENT + 2
round_timer = pygame.USEREVENT + 3

pygame.time.set_timer(bg_timer,50)

# Global Variables for Animation
animate_flag = [0,0,0,0]
animate_alpha = [255,255,255,255]
catch_typing = ""
typing_array = [type_1,type_2,type_3,type_4]

def typing_sfx():
    global catch_typing
    global typing_array
    while True:
        scape = random.choice(typing_array)
        if scape != catch_typing:
            catch_typing = scape
            catch_typing.play()
            break


def draw_bg(surface=None,rect=None,bg=images['menu_bg'],draw_logo=True,color=BEIGE):
    SCREEN.fill((color))
    SCREEN.blit(bg,(0,bg_y))
    SCREEN.blit(bg,(0,bg_y-bg_height+6))
    if surface is not None and rect is not None:
        SCREEN.blit(surface,rect)
    if draw_logo:
        SCREEN.blit(images['logo'],logo_rect)


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
        draw_bg(images['mechanics_bg'],mechanics_bg_rect)
        pygame.display.update()
        clock.tick(FPS)
        

def define_player_window():
    btn_rects = [[images['number_two'],images['number_two_hover'],number_two_rect,False,2],
                     [images['number_three'],images['number_three_hover'],number_three_rect,False,3],
                     [images['number_four'],images['number_four_hover'],number_four_rect,False,4]]
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
                
        draw_bg(images['loading_bg'],loading_bg_rect)

        waiting_label = inria_italic_40.render("Chose the Player Size",1,'Black')
        SCREEN.blit(waiting_label,(332,419))

        mx, my = pygame.mouse.get_pos()
        
        for rect in btn_rects:
            SCREEN.blit(rect[0],rect[2])
            if rect[2].collidepoint(mx,my):
                if not rect[3]:
                    btn_sfx_hover.play()
                    rect[3] = True 
                    for other_rect in btn_rects:
                        if other_rect is not rect:
                            other_rect[3] = False
                SCREEN.blit(rect[1],rect[2]) 
                if lmb_clicked:
                    btn_sfx_click.play()
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
    global animate_flag
    pygame.time.set_timer(loading_timer, 830)  # every 50 frames (50/60)
    waiting = True
    loading_array = [0, 0, 0, 0, 0]

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    animate_flag[0] = 2
            """
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
        draw_bg(images['loading_bg'], loading_bg_rect)

        game_id = game.get_id()
        game_number = lalezar_35.render(f'Game {game_id}', 1, 'black')
        game_number_rect = game_number.get_rect(center=(WIDTH/2,420))
        SCREEN.blit(game_number, game_number_rect)

        waiting_label = inria_italic_40.render('Waiting for Players', 1, 'black')
        SCREEN.blit(waiting_label, (347, 444))

        player_count = game.get_player_count()
        player_size = game.get_player_size()
        player_count_text = f'{player_count}/{player_size}'
        player_count_render = inria_italic_40.render(player_count_text, 1, 'Black')
        SCREEN.blit(player_count_render, (483, 500))


        for i in range(0, len(loading_array)):
            selected_icon = images['loading_0'] if loading_array[i] == 0 else images['loading_1']
            SCREEN.blit(selected_icon, (358 + (67 * i), 576))
            

        pygame.display.update()
        clock.tick(FPS)

        try:
            data = network.receive_game_data()
        except:
            waiting = False
            print('[Waiting for Players]: Something went wrong.')
            return

        if not isinstance(data,Game):
            continue
        
        game = data
        
        waiting = game.get_player_count() < game.get_player_size()

    pygame.time.set_timer(loading_timer, 0) # Disable timer
    game_proper(game)


def fetch_games():
    try:
        return network.send_and_receive("fetch games")
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
        
        draw_bg(images['mechanics_bg'],mechanics_bg_rect)
        games = fetch_games()

        if isinstance(games, dict) and len(games) > 0:
            game_box_rects = []
            count, x, y = 1, 0, 340
            circle = images['circle_waiting']

            for game_id, game in games.items():
                game_number = lalezar_35.render(f'Game {game_id}',1,'black')
                p_count = game.get_player_count()
                p_size = game.get_player_size()
                player_count_text = f'{p_count}/{p_size}'
                player_count_surf = lalezar_35.render(player_count_text,1,'Black')
                
                if p_count == p_size: circle = images['circle_full']
                
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
                    SCREEN.blit(images['game_box_hover'],rect[0])
                    if lmb_clicked:
                        btn_sfx_click.play()
                        join_game(rect[4])
                else: 
                    SCREEN.blit(images['game_box'],rect[0])
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


def send_message(message, receive=True):
    try:
        if receive: return network.send_and_receive(message)
        network.send(message)
    except Exception as e:
        print(f'Failed to send message: {e}')

def request_index(message):
    while True:
        try:
            data = network.send_and_receive(message[0])
            if isinstance(data,int):
                print(f'received index {data}')
                message[0] = data
                break
        except Exception as e:
            print(f'Failed to request index: {e}')

def check_answer_similarity(to_check, to_refer):
    #max score = 100
    #min score = 0
    #returns percentage of answer similarity
    i = 0
    score = 0
    if len(to_check) != len(to_refer): return 0
    while i < len(to_refer):
        if to_check[i].isalpha():
            if to_check[i].lower() == to_refer[i].lower():
                score += 1/len(to_refer)
        elif to_check[i] == to_refer[i]: 
            score += 1/len(to_refer)
        i += 1
    
    score = round(score, 1)
    return score * 100


def game_proper(game: Game):
    # Temporary max input length
    # ideal: dynamically set when client can receive answers from server
    notifcation.play()
    manager = None
    answer_input = TextInputVisualizer(manager,lalezar_50,cursor_width=0)
    
    QnA = game.get_qna()
    round_score = 0
    index = 0   # test
    data = None
    
    while True:
        data = send_message('index')
        if isinstance(data,int):
            index = data
            break
        
    time_limit = 10000
    pygame.time.set_timer(round_timer,time_limit,1)
    timer_start_time = pygame.time.get_ticks()
    score_sent = False
    timer_stopped = False  
    thread_started = False
    
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
                if event.key == pygame.K_RETURN:
                    print("yeet")
                # typing_sfx should only appear when highlighted sob
                typing_sfx()
            
            if event.type == round_timer:   # time's up
                if not score_sent: # didnt guess correctly within the time limit
                    data = send_message(f'score,{round_score}')
                    if isinstance(data,Game): game = data
                    score_sent = True
                round_score = 0
                time_limit = 10000
                timer_stopped = True
                
        if timer_stopped:
            if not thread_started:
                print('starting thread')
                request = ['index']
                thread = Thread(target=request_index, args=(request,))
                thread.start()
                thread_started = True
            if isinstance(request[0],int): 
                index = request[0]
                pygame.time.set_timer(round_timer,time_limit,1)
                timer_start_time = pygame.time.get_ticks()
                timer_stopped = False
                score_sent = False
                thread_started = False
        else:
            data = receive_game_data()
            if isinstance(data,Game): game = data 
                    
        draw_bg(bg=images['game_bg'],draw_logo=False,color=BLUE)
        SCREEN.blit(images['question_box'],(23,18))
        
        question_surf = inria_50.render(QnA[index][0],1,'black',wraplength=qbox_width-10)
        question_rect = question_surf.get_rect(center=(WIDTH/2,qbox_height/2))
        SCREEN.blit(question_surf,question_rect)
        
        draw_players(game)
        
        SCREEN.blit(images['answer_box'],(23,669))
        answer_input_rect = answer_input.surface.get_rect(center=(WIDTH/2,715))
        SCREEN.blit(answer_input.surface,answer_input_rect)
        answer_input.update(events)
        
        # guessed correctly before the time limit
        # insert the answer verifier
        similarity_result = check_answer_similarity(answer_input.value, QnA[index][1])
        if similarity_result > 0 and not score_sent:
            elapsed_time = pygame.time.get_ticks() - timer_start_time
            correct.play()
            if elapsed_time <= 5000: round_score = 100
            else: round_score = 50

            round_score *= similarity_result

            data = send_message(f'score,{round_score}')
            if isinstance(data,Game): game = data
            score_sent = True
            
        pygame.display.update()
        clock.tick(FPS)

def leaderboard():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == bg_timer:
                scroll_bg()

        draw_bg(bg=images['game_bg'],draw_logo=True,color=BLUE)

def receive_game_data():
    try:
        return network.receive_game_data()
    except:
        print('Something went wrong. Restarting network...')
        # idk if this works
        restart_network()
        main_menu()
    
    
def send_score(round_score):
    try:
        return network.send_and_receive(f'score,{round_score}')
    except Exception as e: 
        print(f'Failed to send score: {e}')


def draw_players(game:Game):
    global animate_flag
    global animate_alpha
    players = game.get_players()
    card_x, card_y = 23, 494
    name_x, name_y = 35, 562
    score_x, score_y = 35, 602
    counter = 1
    card_array = ['player_card_1','player_card_2','player_card_3','player_card_4']
    alpha_array = ['player_card_1_alpha','player_card_2_alpha','player_card_3_alpha','player_card_4_alpha']
    for id, data in players.items():
        name = lalezar_30.render(data['name'],1,'black')
        score = lalezar_30.render(str(data['score']),1,'black')
        player_card_holder = 'player_card_' + str(counter)
        
        # If animation_flag == 0, proceed as normal
        # else, if 2, then its normal to alpha
        # else, if 1, then its alpha to normal
        if animate_flag[counter-1] == 0:
            SCREEN.blit(images[player_card_holder],(card_x,card_y))
        else:
            front_to_invisible = images[card_array[counter-1]].convert_alpha()
            front_to_invisible.set_alpha(animate_alpha[counter-1])

            back_to_visible = images[alpha_array[counter-1]].convert_alpha()
            back_to_visible.set_alpha(255 - animate_alpha[counter-1])
            
            SCREEN.blit(front_to_invisible,(card_x,card_y))
            SCREEN.blit(back_to_visible,(card_x,card_y))
            if animate_flag[counter-1] == 2:
                animate_alpha[counter-1] -= 13
                if animate_alpha[counter-1] < 0:
                    animate_alpha[counter-1] = 0
                    animate_flag[counter-1] -= 1
            else:
                animate_alpha[counter-1] += 13
                if animate_alpha[counter-1] > 255:
                    animate_alpha[counter-1] = 255
                    animate_flag[counter-1] -= 1
        
        SCREEN.blit(name,(name_x,name_y))
        SCREEN.blit(score,(score_x,score_y))
        card_x += 248
        name_x += 248
        score_x += 248
        counter += 1

def draw_leaderboard(game:Game):
    players = game.get_players()
    card_x, card_y = 32, 18
    name_x, name_y = 44, 86
    score_x, score_y = 44, 126
    counter = 1
    for id, data in players.items():
        name = lalezar_30.render(data['name'],1,'black')
        score = lalezar_30.render(str(data['score']),1,'black')
        player_card_holder = 'player_card_' + str(counter)
        SCREEN.blit(images[player_card_holder],(card_x,card_y))
        SCREEN.blit(name,(name_x,name_y))
        SCREEN.blit(score,(score_x,score_y))
        card_y += 192
        name_y += 192
        score_y += 192
        counter += 1
    
    
# Scrolling background effect
def scroll_bg():
    global bg_y
    bg_y += 1
    if bg_y > bg_height:
        bg_y = 0  


def restart_network():
    global network 
    network = Network(server_ip)
    
    
def main_menu():
    field_clicked = False
    name_input.cursor_visible = False
    btn_rects = [[images['create_btn'],images['create_btn_hover'],create_btn_rect,False],
                     [images['join_btn'],images['join_btn_hover'],join_btn_rect,False],
                     [images['mechanics_btn'],images['mechanics_btn_hover'],mechanics_btn_rect,False]]
    
    bgm_sound.play(loops=-1)
    
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
        name_label = inria_italic_20.render('Hello there,', True, (0,0,0))
        name_label_rect = name_label.get_rect(topleft=(325,301))
        SCREEN.blit(name_label, name_label_rect)
        SCREEN.blit(images['name_field'], name_field_rect)
        SCREEN.blit(name_input.surface,(325,332))
        
        mx, my = pygame.mouse.get_pos()
        
        # Buttons
        for rect in btn_rects: 
            SCREEN.blit(rect[0],rect[2])
            if name_input.value != '':
                if rect[2].collidepoint(mx,my):
                    if rect[3] is False:
                        btn_sfx_hover.play()
                        rect[3] = True
                        for other_rect in btn_rects:
                            if other_rect is not rect:
                                other_rect[3] = False 
                    SCREEN.blit(rect[1],rect[2])
                    if lmb_clicked:
                        btn_sfx_click.play()
                        if rect[0] is images['create_btn']:
                            define_player_window()
                        elif rect[0] is images['join_btn']:
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

def animate_player_card(card,card_alpha,pos_x,pos_y,counter,alpha,frames):
    if counter < 2:
        if counter == 0:             
                
            card_1_with_alpha = images[card].convert_alpha()
            card_1_with_alpha.set_alpha(alpha)

            card_2_with_alpha = images[card_alpha].convert_alpha()
            card_2_with_alpha.set_alpha(255 - alpha)

            SCREEN.blit(card_1_with_alpha,(pos_x,pos_y))
            SCREEN.blit(card_2_with_alpha,(pos_x,pos_y))

            alpha -= 13
            if alpha < 0:
                alpha = 0
                counter += 1
                
        elif counter == 1:
                
            card_1_with_alpha = images[card_alpha].convert_alpha()
            card_1_with_alpha.set_alpha(255 - alpha)

            card_2_with_alpha = images[card].convert_alpha()
            card_2_with_alpha.set_alpha(alpha)


            #SCREEN.blit(images[card],(pos_x,pos_y))
            SCREEN.blit(card_1_with_alpha,(pos_x,pos_y))
            SCREEN.blit(card_2_with_alpha,(pos_x,pos_y))

            alpha += 16
            if alpha > 275:
                counter += 1
    else:
        SCREEN.blit(images[card],(pos_x,pos_y))

    return counter, alpha

def animate_card2(card_id,label_array):
    global animate_flag
    global card_rect_array
    global score_rect_array
    global label_rect_array
    reverse_flag = 0
    card_array = ['player_card_1','player_card_2','player_card_3','player_card_4']
    alpha_array = ['player_card_1_alpha','player_card_2_alpha','player_card_3_alpha','player_card_4_alpha']
    if animate_flag[card_id] == 0:
        alpha = 255
        animate_flag[card_id] = 1
        for i in range(0,20):
            print(alpha)
            front_to_invisible = images[card_array[card_id]].convert_alpha()
            front_to_invisible.set_alpha(alpha)

            back_to_visible = images[card_array[card_id]].convert_alpha()
            back_to_visible.set_alpha(255 - alpha)

            #SCREEN.blit(front_to_invisible,card_rect_array[card_id])
            #SCREEN.blit(back_to_visible,card_rect_array[card_id])
            
            SCREEN.blit(front_to_invisible,(0,0))
            SCREEN.blit(back_to_visible,(0,0))

            alpha -= 13
            if alpha < 0:
                alpha = 0
        animate_flag[card_id] = 0
    else:
        pass

def player_name():
    screen_transition.play()
    enter_btn_hovered = False
    flag = 0
    alpha = 255
    counter = 0
    frames = 0
    while True:
        lmb_clicked = False
        player_name_value = name_input.value
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name_value != '':
                    btn_sfx_click.play()
                    screen_transition.play()
                    main_menu()
                # typing_sfx should only appear when highlighted sob
                typing_sfx()

        draw_bg(images['loading_bg'],loading_bg_rect)

        # Label
        window_label = inria_italic_40.render("Enter Your Name",1,'Black')
        SCREEN.blit(window_label,(365,419))
        
        # Namebox and Button
        SCREEN.blit(images['name_box'],name_box_rect)
        SCREEN.blit(images['enter_btn'],enter_btn_rect)

        """
        # animation should be shown locally sobberns
        counter, alpha = animate_player_card('player_card_4','player_card_4_alpha',0,400,counter,alpha,frames)
        frames += 1
        """

        
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
                    enter_btn_hovered = True
                    btn_sfx_hover.play()
                SCREEN.blit(images['enter_btn_hover'], enter_btn_rect)
                if lmb_clicked:
                    print(player_name_value,"has opened the game")
                    btn_sfx_click.play()
                    screen_transition.play()
                    main_menu()
            else: 
                enter_btn_hovered = False
                
        pygame.display.update()
        clock.tick(FPS)

def ip_input_scene():
    enter_btn_hovered = False
    flag = 0
    alpha = 255
    counter = 0
    frames = 0
    
    manager = TextInputManager(validator=lambda input: len(input) <= 15)
    ip_input = TextInputVisualizer(manager,lalezar_30,cursor_width=0)
    
    
        
    while True:
        lmb_clicked = False
        ip_value = ip_input.value
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and ip_value != '':
                    btn_sfx_click.play()
                    if net_test(ip_value):
                        return ip_value
                    else:
                        sfx_error.play()
                        ip_input.value = ""
                # typing_sfx should only appear when highlighted sob
                typing_sfx()

        draw_bg(images['loading_bg'],loading_bg_rect)

        # Label
        window_label = inria_italic_40.render("Enter Server IP",1,'Black')
        SCREEN.blit(window_label,(365,419))
        
        # Namebox and Button
        SCREEN.blit(images['name_box'],name_box_rect)
        SCREEN.blit(images['enter_btn'],enter_btn_rect)

        """
        # animation should be shown locally sobberns
        counter, alpha = animate_player_card('player_card_4','player_card_4_alpha',0,400,counter,alpha,frames)
        frames += 1
        """

        
        # Render player name on the screen
        ip_surf = ip_input.surface
        ip_rect = ip_surf.get_rect(center=(WIDTH/2,517))
        SCREEN.blit(ip_input.surface,ip_rect)
        ip_input.update(events)

        mx, my = pygame.mouse.get_pos()
        
        # Handle button hover & sfx
        if ip_value != '':
            if enter_btn_rect.collidepoint(mx, my):
                if not enter_btn_hovered:
                    btn_sfx_hover.play()
                    enter_btn_hovered = True
                SCREEN.blit(images['enter_btn_hover'], enter_btn_rect)
                if lmb_clicked:
                    btn_sfx_click.play()
                    if net_test(ip_value):
                        return ip_value
                    else:
                        sfx_error.play()
                        ip_input.value = ""
                        
            else: 
                enter_btn_hovered = False
                
        pygame.display.update()
        clock.tick(FPS) 

def end_screen(game:Game):
    highlight_name = "John Kekow"
    
    bgm_sound.stop()
    victory.play()    
    
    while True:
        lmb_clicked = False
        player_name_value = name_input.value
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name_value != '':
                    btn_sfx_click.play()
                    main_menu()

        # Draw the screen
        draw_bg(bg=images['game_bg'], draw_logo=False,color=BLUE)

        # need to call the highest score from sever
        # Label
        window_label = inria_italic_40.render(highlight_name,2,'White')
        text_w, text_h = window_label.get_size()
        x_center = ((691 - text_w) // 2) + 294
        victory_b = images['victory_b'].get_rect(topleft = (x_center+(text_w)+17,301))
        SCREEN.blit(window_label,(x_center,298))

        SCREEN.blit(images['congrats_label'], congrats_label_rect)
        SCREEN.blit(images['congrats_label_2'], win_label_rect)

        victory_a = images['victory_a'].get_rect(topleft = (x_center-(text_w // 2)+17,301))
        
        SCREEN.blit(images['victory_a'], victory_a)
        SCREEN.blit(images['victory_b'], victory_b)


        mx, my = pygame.mouse.get_pos()
        # Handle button hover & sfx
        if exit_game_btn_rect.collidepoint(mx, my):
            if not enter_btn_hovered:
                btn_sfx_hover.play()
                enter_btn_hovered = True
            SCREEN.blit(images['exit_game_hover'], exit_game_btn_rect)
            if lmb_clicked:
                btn_sfx_click.play()
                main_menu()
        else: 
            enter_btn_hovered = False
            SCREEN.blit(images['exit_game_btn'], exit_game_btn_rect)
        
        # need to also send score to players yeet
        draw_leaderboard(game)

        pygame.display.update()
        clock.tick(FPS)

server_ip = ip_input_scene()
network = Network(server_ip)
player_name()
