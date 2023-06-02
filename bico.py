#-*-coding: utf-8
import pygame
import os
import random
from math import floor
import sys
loc = os.path.dirname(os.path.abspath(__file__))

name_list = ["효서 코인","재원 코인","효원 코인","조쉬 코인","매캔티 코인"]
not_using_name = 4
hand_list = [1,5,10,50,100,500,1000]

def market_update():
    for i in coins:
        i[2] = i[1]
        i[1] += round(random.random() *1.05* i[1] - round(i[1]/2))
        if i[2] == 0:
            i[2] = 1

pygame.init()

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("시크릿 주주")

clock = pygame.time.Clock()

background = pygame.image.load(f"{loc}/image/background.png")

time_font = pygame.font.SysFont(None, 30)
money_font = pygame.font.SysFont(None, 45)
name_font = pygame.font.SysFont("hansantteutdotum", 20)
price_font = pygame.font.SysFont(None, 30)
updown_font = pygame.font.SysFont(None, 25)
number_font = pygame.font.SysFont(None, 25)
ex_font = pygame.font.SysFont(None, 20)
sign_font = pygame.font.SysFont("hansantteutdotum", 11)

white = (255,255,255)
grey = (100,100,100)
up_color = (231, 25,9)
down_color = (17,91,203)


countdown = 10
money = 5000
coins = [] # 이름, 현 가격, 전가격, 보유 개수, 텍스트
buttons = []
hand_size = 1
date = 1
boost = 1
tax = 1/100

for i in range(4):
    coins.append([name_list[i], 100, 100, 0,[None,None,None,None]])
    buttons.append([pygame.image.load(f"{loc}/image/buy.png"),pygame.image.load(f"{loc}/image/sell.png"),None,None])


running = True
while running:

    dt = clock.tick(24)

    if countdown > 0:
        countdown -= 1/24 * boost
    else:
        for i in coins:
            if i[1] == 0:
                if i[0] == "준비중...":
                    nm = coins.index(i)
                    coins[coins.index(i)][3] = 0
                    coins[coins.index(i)][1] = 100
                    coins[coins.index(i)][2] = 100
                    coins[coins.index(i)][0] = name_list[not_using_name]
                    not_using_name = nm
                else:
                    coins[coins.index(i)][0] = "준비중..."
                    coins[coins.index(i)][3] = 0
        countdown = 20
        date += 1
        market_update()

    for i in coins:
        if i[1] < 5:
            i[1] = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_pos = pygame.mouse.get_pos()
                for i in buttons:
                    if i[2].collidepoint(m_pos):
                        if money >= coins[buttons.index(i)][1] * hand_size:
                            money -= coins[buttons.index(i)][1] * hand_size
                            coins[buttons.index(i)][3] += 1 * hand_size

                    elif i[3].collidepoint(m_pos):
                        if coins[buttons.index(i)][3] >= 1 * hand_size:
                            coins[buttons.index(i)][3] -= 1 * hand_size
                            money += (coins[buttons.index(i)][1] * hand_size ) * (1-tax)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                hand_size = hand_list[hand_list.index(hand_size)-6]
            elif event.key == pygame.K_DOWN:
                hand_size = hand_list[hand_list.index(hand_size)-1]
            elif event.key == pygame.K_SPACE:
                if boost == 1:
                    boost = 4
                elif boost == 4:
                    boost = 1
    for i in buttons:
        i[2] = i[0].get_rect()
        i[2].left,i[2].top = (580, 110+83*buttons.index(i))
        i[3] = i[1].get_rect()
        i[3].left,i[3].top = (680, 110+83*buttons.index(i))

    for i in coins:
        i[4][0] = name_font.render(i[0],True,white)
        i[4][1] = price_font.render(f"{i[1]} G",True,white)
        i[4][2] = updown_font.render(f"{round((i[1]*100/i[2])-100,2)} %",True,white)
        i[4][3] = number_font.render(f"stock : {i[3]}",True,grey)
    
    expect_money = money
    for i in coins:
        expect_money += i[1]*i[3]*99/100
        
    cd_text = time_font.render(f"{floor(countdown)} ",True,white)
    money_text = money_font.render(f"{round(money)} G", True, white)
    expect_money_text = ex_font.render(f"{round(expect_money)} G", True, grey)
    hs_text = ex_font.render(f"{hand_size}",True, white)
    date_text = time_font.render(f"day {date}",True, white)
    up_text = sign_font.render(u"▲",True,up_color)
    down_text = sign_font.render(u"▼",True,down_color)
    stay_text = sign_font.render(u"━",True,grey)
    

    screen.blit(background, (0, 0))
    
    screen.blit(cd_text,(screen_width-10-cd_text.get_rect().size[0], 10))
    screen.blit(date_text,(screen_width-50-date_text.get_rect().size[0], 10))
    screen.blit(money_text,(440-money_text.get_rect().size[0], 345-money_text.get_rect().size[1]))
    screen.blit(expect_money_text,(440-expect_money_text.get_rect().size[0], 380-money_text.get_rect().size[1]))
    screen.blit(hs_text,(770-hs_text.get_rect().size[0],50))

    for i in coins:
        screen.blit(i[4][0],(475, 74+83*coins.index(i)))
        screen.blit(i[4][1],(770-i[4][1].get_rect().size[0], 75+83*coins.index(i)))
        screen.blit(i[4][2],(670-i[4][2].get_rect().size[0], 80+83*coins.index(i)))
        screen.blit(i[4][3],(473, 115+83*coins.index(i)))
        screen.blit(buttons[coins.index(i)][0],(580, 110+83*coins.index(i)))
        screen.blit(buttons[coins.index(i)][1],(680, 110+83*coins.index(i)))
        if i[1]-i[2] > 0:
            screen.blit(up_text,(590, 80+83*coins.index(i)))
        elif i[1]-i[2]<0:
            screen.blit(down_text,(590, 80+83*coins.index(i)))
        else:
            screen.blit(stay_text,(590, 80+83*coins.index(i)))


    pygame.display.update() 


pygame.quit()