import pygame
import random
import math
from pygame import mixer

#initialise pygame
pygame.init()

#create screen
screen=pygame.display.set_mode((800, 600))

# bg
bgimg=pygame.image.load('bg.jpg')
DEFAULT_IMAGE_SIZE3= (800, 600)
bgimg=pygame.transform.scale(bgimg, DEFAULT_IMAGE_SIZE3)

#bg sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('spaceship.png')
DEFAULT_IMAGE_SIZE= (75, 80)
playerImg=pygame.transform.scale(playerImg, DEFAULT_IMAGE_SIZE)
px_change=0
px=370
py=480

#enemy
enemyImg=[]
ex=[]
ey=[]
ex_change=[]
ey_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg1=pygame.image.load('alien.png')
    DEFAULT_IMAGE_SIZE2= (64, 64)
    enemyImg.append(pygame.transform.scale(enemyImg1, DEFAULT_IMAGE_SIZE2))
    ex_change.append(0.4)
    ey_change.append(40)
    ex.append(random.randint(0,736))
    ey.append(random.randint(50, 150))


#bullet

#READY== u cant see bullet on screen
#FIRE== bullet is fired

bulletImg=pygame.image.load('bullet.png')
DEFAULT_IMAGE_SIZE4= (44, 32)
bulletImg=pygame.transform.scale(bulletImg, DEFAULT_IMAGE_SIZE4)
bx_change=0
by_change=1
bx=0
by=480
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf', 32)
textx=10
texty=10

#game over text
gofont=pygame.font.Font('freesansbold.ttf', 96)


def show_score(x,y):
    score=font.render("Score: "+ str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text=font.render("Game Over!", True, (190,0,50))
    screen.blit(over_text, (300,250))

def player(x, y):
    screen.blit(playerImg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(ex, ey, bx, by):
    distance= math.sqrt(math.pow(ex-bx,2)+math.pow(ey-by,2))
    if distance<27:
        return True
    else:
        return False

#Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        # if key stroke is pressed, check left or right
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                px_change=-0.5
            if event.key==pygame.K_RIGHT:
                px_change= 0.5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bsound=mixer.Sound('laser.wav')
                    bsound.play()
                    bx=px
                    fire_bullet(bx, by)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                px_change= 0

    screen.fill((100,15,150))
    #bg img
    screen.blit(bgimg, (0,0))
    
    #player movement
    px+=px_change

    if px<=0:
        px=0
    elif px>=725:
        px=725

    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if ey[i]>440:
            for j in range(num_of_enemies):
                ey[j]=2000
            game_over_text()
            break

        ex[i]+=ex_change[i]
        if ex[i]<=0:
            ex_change[i]=0.4
            ey[i]+=ey_change[i]
        elif ex[i]>=736:
            ex_change[i]=-0.4
            ey[i]+=ey_change[i]

        #collision
        collision=isCollision(ex[i],ey[i],bx,by)
        if collision:
            exp_sound=mixer.Sound('explosion.wav')
            exp_sound.play()
            by=480
            bullet_state="ready"
            score_value+=1
            print(score_value)
            ex[i]=random.randint(0,800)
            ey[i]=random.randint(50, 150)

        enemy(ex[i], ey[i], i) 

    #bullet movement
    if by<=0:
        by=480
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet(bx, by)
        by-=by_change

    


    player(px, py)
    show_score(textx, texty) 
    pygame.display.update()
