import pygame, sys
from pygame.locals import *
import random
import math
from pygame import mixer

#initialising pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.png')
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1) 

#title & icon

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('space-invaders.png')
playerX=370
playerY=480
playerX_change=5

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemy_changeX=[]
enemy_changeY=[]
no_of_enemies=6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemy_changeX.append(3)
    enemy_changeY.append(40)

#bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bullet_changeY=10
#ready - you can't see the bullet on the screen
#Fire - the bullet is in moving state
bullet_state="ready"

# score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

# game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text= over_font.render("GAME OVER :(" ,True,(255,255,255))
    screen.blit(over_text, (200,250))
    


def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX,enemyY,playerX,playerY):
    distance=math.sqrt((math.pow(bulletX - enemyX,2))+(math.pow(bulletY- enemyY,2)))
    if distance < 27:
        return True
    else:
        return False
#game loop
running = True
while running:
	#color system(R,G,B)
    screen.fill((0,0,0))
    # background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

		# if keystroke is pressed,check whether it is right or left
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change=-5
            if event.key == pygame.K_RIGHT:
                playerX_change=5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound =mixer.Sound('laser.wav')
                    bullet_sound.play()
                	# bulletX gets the current x coordinate of axis.
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0

    playerX +=playerX_change

    #creating boundaries for space invader(player) so , it doesn't go out of bound.
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    #enemy movement
    for i in range(no_of_enemies):

        # game over :(
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j]=2000

            game_over_text()
            break

        enemyX[i]+= enemy_changeX[i]
        if enemyX[i] <=0:
            enemy_changeX[i]=4
            enemyY[i]+= enemy_changeY[i]
        elif enemyX[i] >=736:
            enemy_changeX[i]=-4
            enemyY[i]+ enemy_changeY[i]
        # collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value +=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)
        
    #bullet movement
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-= bullet_changeY


        
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()