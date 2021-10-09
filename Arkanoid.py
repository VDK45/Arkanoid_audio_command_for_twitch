import sys
import os
import pygame
from random import randrange as rnd
import time
import threading
from threading import Timer
import twitch_bot
import Audio_assistant as aa

thread1 = threading.Thread(target=twitch_bot.run, args=())
thread1.start()
##thread2 = threading.Thread(target=aa.run, args=())
##thread2.start()

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




WIDTH, HEIGHT = 1280, 720
fps = 24
# Text
pygame.font.init() 
tf2build_font1 = resource_path('resource/tf2build.ttf')
tf2secondary_font1 = resource_path('resource/tf2secondary.ttf')
smallfon = pygame.font.Font(tf2build_font1, 18)
myfont  = pygame.font.Font(tf2build_font1, 16)
#textsurface = myfont.render('Пишите в чат: !left или !right чтобы начать игру!', False, (255, 255, 0))
textsurface2 = myfont.render('Write to chat: !Left or !Right to start the game!', False, (255, 0, 255))
textpaddle = myfont.render(f'{twitch_bot.chater}:  {twitch_bot.message}', False, (255, 255, 80))

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



reset = False
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    sc.fill((0, 255, 0)) 
    sc.blit(img, (0, 0))
   
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
        # special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 0
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
    if key[pygame.K_ESCAPE]:
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
    
    # TEXT
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
    clock.tick(fps)
    keys = pygame.key.get_pressed()
    keys_pres = pygame.key.get_pressed()
    # pygame.time.delay(50)
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            loop = False
        if keys_pres[pygame.K_ESCAPE]:
            loop = False
    
    



print('Game stoped')
pygame.quit()
