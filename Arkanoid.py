#!/usr/bin/python3.9
# Setup Python ----------------------------------------------- #
import sys
import os
import pygame
from random import randrange as rnd
import time
import threading
from threading import Timer
import pyperclip
import twitch_bot

import Audio_assistant as aa
import webbrowser

##f = open('config.py', 'w')
##f.write('HOST = "irc.twitch.tv"\n')
##f.write('PORT = 6667\n')
##f.write('NICK = "bot"\n')
##f.write('RATE = (20/30)\n')
##f.write('oplist = {"username":[""]}\n')
##f.close()

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

WIDTH, HEIGHT = 1280, 720
# Text
pygame.font.init() 
tf2build_font1 = resource_path('resource/tf2build.ttf')
tf2secondary_font1 = resource_path('resource/tf2secondary.ttf')
smallfon = pygame.font.Font(tf2build_font1, 18)
myfont  = pygame.font.Font(tf2build_font1, 16)
font  = pygame.font.Font(tf2build_font1, 30)
font2  = pygame.font.Font(tf2build_font1, 50)
# textsurface = myfont.render('Пишите в чат: !left или !right чтобы начать игру!', False, (255, 255, 0))
textsurface2 = myfont.render('Write to chat: !Left or !Right to start the game!', False, (255, 0, 255))
textpaddle = myfont.render(f'{twitch_bot.chater}:  {twitch_bot.message}', False, (255, 255, 80))
# paddle settings
paddle_w = 500
paddle_h = 50
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h, paddle_w, paddle_h)
# ball settings
ball_radius = 20
ball_speed = 1
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
# blocks settings
block_list = [pygame.Rect(50 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(2)]
color_list = [(rnd(30, 256), rnd(30, 200), rnd(30, 256)) for i in range(10) for j in range(2)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# background image
background = resource_path('resource/screen.png')
img = pygame.image.load(background).convert()


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

# Sound
pygame.mixer.init()
sms_sound = resource_path("sound/sms.wav")
sms = pygame.mixer.Sound(sms_sound)

def show_command(x, y, chater, message):
    message = myfont.render(f'{chater}:  {message}', True, (0, 255, 255))
    sc.blit(message, (x, y))

def show_chat(x, y, chater, message):
    global count_chat
    message = smallfon.render(f'{chater}:  {message}', True, (255, 255, 255))
    sc.blit(message, (x, y))
# Ativate modules
thread1 = threading.Thread(target=twitch_bot.run, args=())
thread1.start()
thread2 = threading.Thread(target=aa.run, args=())
thread2.start()
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Arkanoid for  Twitch chat play')
screen = pygame.display.set_mode((1280, 720),0,32)
# Colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False

text_hind = 'OAuth Password'
def main_menu():
    
    while True:
        global click
        screen.fill((0, 255, 0))
        draw_text('Menu', font, (0, 0, 255), screen, 80, 30)
        
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 250, 50)
        button_3 = pygame.Rect(50, 300, 300, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                chanel()
        if button_3.collidepoint((mx, my)):
            if click:
                password()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                twitch_bot.loop_true = False # Stop twitch bot
                twitch_bot.send_mess('ARKANOID has stopped')
                aa.assis = False # Audio assis stop
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    twitch_bot.loop_true = False # Stop twitch bot
                    twitch_bot.send_mess('ARKANOID has stopped')
                    aa.assis = False # Audio assis stop
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        draw_text('Game', font, (255, 255, 255), screen, 80, 115)
        draw_text('Chanel', font, (255, 255, 255), screen, 80, 215)
        draw_text('Password', font, (255, 255, 255), screen, 80, 315)
        pygame.display.update()
        mainClock.tick(60)
 
def game():
    # paddle settings
    paddle_w = 500
    paddle_h = 50
    paddle_speed = 15
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h, paddle_w, paddle_h)
    # ball settings
    ball_radius = 20
    ball_speed = 1
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    # blocks settings
    block_list = [pygame.Rect(50 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(2)]
    color_list = [(rnd(30, 256), rnd(30, 200), rnd(30, 256)) for i in range(10) for j in range(2)]

    reset = False
    running = True
    while running:
        screen.fill((0,255,0))
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                twitch_bot.loop_true = False # Stop twitch bot
                twitch_bot.send_mess('ARKANOID has stopped')
                aa.assis = False # Audio assis stop
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        # drawing world
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # collision left right
        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx
        # collision top
        if ball.centery < ball_radius:
            dy = -dy
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        # collision blocks
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)

        # win, game over
        if ball.bottom > HEIGHT:
            print('GAME OVER!')
            reset = True
            ball.x = paddle.left + paddle_w // 2 - 25
            ball.y = 636
            block_list.clear()
            block_list = [pygame.Rect(50 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(2)]
            color_list = [(rnd(30, 256), rnd(30, 200), rnd(30, 256)) for i in range(10) for j in range(2)]
            dx, dy = 0, 0
            #exit()
        elif not len(block_list):
            print('WIN!!!')
            reset = True
            ball.x = paddle.left + paddle_w // 2 - 25
            ball.y = 636
            block_list.clear()
            block_list = [pygame.Rect(50 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(2)]
            color_list = [(rnd(30, 256), rnd(30, 200), rnd(30, 256)) for i in range(10) for j in range(2)]
            dx, dy = 0, 0
            #exit()
                
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
            if reset == True:
                dx, dy = 1, -1
            reset = False
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed
            if reset == True:
                dx, dy = -1, -1
            reset = False
        if key[pygame.K_BACKSPACE]:
            loop = False
            twitch_bot.loop_true = False # Stop twitch bot
            aa.assis = False # Audio assis stop
        # Twitch control
        if twitch_bot.command == '!left' and paddle.left > 0 or twitch_bot.command == '!l' and paddle.left > 0:
            paddle.left -= paddle_speed
            if reset == True:
                dx, dy = 1, -1
            reset = False
        if twitch_bot.command == '!right' and paddle.right < WIDTH or twitch_bot.command == '!r' and paddle.right < WIDTH:
            paddle.left += paddle_speed
            if reset == True:
                dx, dy = 1, -1
            reset = False

        try:
            if twitch_bot.sound == True :
                sms.play()
        except IndexError:
            continue
            
        #  SHOW COMMANDS at paddle
        if reset == True:
            #sc.blit(textsurface,(50,570))
            sc.blit(textsurface2,(paddle.left + 20,700))
        if twitch_bot.message[:1] == '!' and twitch_bot.chater != 'nightbot' and len(twitch_bot.command) <= 10:
            show_command(paddle.left + 170, 680, twitch_bot.chater, twitch_bot.message)
            
        show_chat(15, 390, twitch_bot.lst_chat[6], twitch_bot.lst_chat[7])
        show_chat(15, 410, twitch_bot.lst_chat[4], twitch_bot.lst_chat[5])
        show_chat(15, 430, twitch_bot.lst_chat[2], twitch_bot.lst_chat[3])
        show_chat(15, 450, twitch_bot.lst_chat[0], twitch_bot.lst_chat[1])
        # update screen
        pygame.display.flip()
##        pygame.display.update()
        mainClock.tick(60)
        keys = pygame.key.get_pressed()
        keys_pres = pygame.key.get_pressed()
        # pygame.time.delay(50)
        

 
def chanel():
    running = True
    font = pygame.font.Font(tf2build_font1, 30)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    while running:
        screen.fill((0,255,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                twitch_bot.loop_true = False # Stop twitch bot
                twitch_bot.send_mess('ARKANOID has stopped')
                aa.assis = False # Audio assis stop
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:

                    if event.key == pygame.K_RETURN:
                        f = open('chanel.txt', 'w+')
                        f.write(f'{text}')
                        f.close()
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0, 255, 0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text('Enter your twitch Chanel!', font, (0, 0, 0), screen, 50, 50)


        
        
        pygame.display.update()
        mainClock.tick(60)

        

def password():
    global text_hind
    running = True
    font = pygame.font.Font(tf2build_font1, 20)
    clock = pygame.time.Clock()

    
    input_box = pygame.Rect(100, 450, 100, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    while running:
        click = False
        screen.fill((0,255,0))
        draw_text('Password', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                twitch_bot.loop_true = False # Stop twitch bot
                twitch_bot.send_mess('ARKANOID has stopped')
                aa.assis = False # Audio assis stop
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    text_hind = 'OAuth Password'
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    text = pyperclip.paste() # Paste password
                    text_hind = ''
                    f = open('password.txt', 'w+')
                    f.write(f'{text}')
                    f.close()
                    #print(text)
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:

                    if event.key == pygame.K_RETURN:
                        text = ''
                        print(text)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        
        screen.fill((0, 255, 0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.

        width = max(200, txt_surface.get_width()+10)
        input_box.w = width

        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        # Text
        draw_text('Attention!', font2, (255, 0, 0), screen, 50, 30)
        draw_text("Do not show your password!", font, (255, 0, 0), screen, 50, 100)
        draw_text("Don't forget to turn off stream!", font, (255, 0, 0), screen, 50, 150)
        draw_text('Get your twitch Password!', font, (0, 0, 0), screen, 50, 250)
        draw_text('Enter your twitch Password:', font, (0, 0, 0), screen, 50, 400)
        draw_text('And reset game!', font, (0, 0, 0), screen, 50, 550)
        # Text hinde
        draw_text(text_hind, font, (255, 255, 255), screen, 110, 465)
        # Get click
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(100, 300, 270, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        draw_text('Get OAuth Password', font, (255, 255, 255), screen, 120, 315)
        if button_1.collidepoint((mx, my)):
            if click:
                print('Connect to Twitch. Please Copy Twitch Chat OAuth Password!')
                print('Example:  oauth:g138k3tlk87z5ji3yu4fq8qv65y95s')
                webbrowser.open('http://twitchapps.com/tmi/')
        click = False
        pygame.display.update()
        mainClock.tick(60)



main_menu()

