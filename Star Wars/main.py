import pygame
import random
import math
from pygame import mixer

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Canberra', 40)

#create the screen
screen = pygame.display.set_mode((800,600))
game_run = 1


# background
background = pygame.image.load(r'C:\Users\ACER\Downloads\background.jpg')

# backgroud sound
mixer.music.load(r"C:\Users\ACER\Desktop\sound\mp3\Le_Castle.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders") 

icon = pygame.image.load(r'C:\Users\ACER\Downloads\falcon.png')
pygame.display.set_icon(icon)

# ===================================================================#


# Player
playerImg1 = pygame.image.load(r'C:\Users\ACER\Downloads\falcon.png')
playerImg = pygame.transform.scale( playerImg1, (90,90))
playerX = 375  #total X is 800
playerY = 480  #total Y is 600
playerX_change = 0


# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change= []
num_of_enemies = 6

for i in range(num_of_enemies):
    k = pygame.image.load(r'C:\Users\ACER\Downloads\stormtrooper.png')
    k1 = pygame.transform.scale(k, (75,70))
    enemyImg.append(k1)
    enemyX.append(random.randint(0,735))  #total X is 800
    enemyY.append(random.randint(50,120))  #total Y is 600
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
can_bullet_fire = "yes"
bullet_count=0
freeze_count = 0
bulletImg = pygame.image.load(r'C:\Users\ACER\Downloads\bullet.png')
bulletX = 0
bulletY = 480

bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_val = 0
font = pygame.font.Font('Starjedi.ttf', 32)

textX = 10
textY = 10


#game over text
over_font = pygame.font.Font('Starjout.ttf', 65)


# ========================================================================= #

def show_score(x,y):
    score = font.render("Score : " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit((bulletImg),(x+29,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

    
def player(x,y):
    screen.blit(playerImg, (x, y))


def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

def game_over_text():
    over_text = over_font.render("GAME oVER", True, (255,255,255))
    screen.blit(over_text, (200,250))
    mixer.music.pause()

def play_again():
    play_again_font = pygame.font.Font('Starjedi.ttf', 38)
    text = play_again_font.render('Play again', 13, (255,255,0))
    global b
    b = pygame.draw.rect(screen, (255,255,255),  ((275, 100), (270, 60)), 1)
    screen.blit(text, (283,99))

loop = True
start_time = None
clock = pygame.time.Clock()

def freeze():
    
    global start_time
    start_time = pygame.time.get_ticks()

def game_start():    
    global game_start_time
    game_start_time = pygame.time.get_ticks()
    print(game_start_time)
    
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    if game_run == 1:
        game_start()
        game_run = game_run+1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            pos = pygame.mouse.get_pos()
            if b.collidepoint(pos):
                print("zone")
                bullet_count = 0
                score = 0
                score_val = 0
                game_run = 1
                can_bullet_fire = "yes"
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0,735)  
                    enemyY[i] = random.randint(50,120)
                    


        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready" and can_bullet_fire != "no":
                    
                    if bullet_count == 15:
                        freeze_count = freeze_count + 1
                        if freeze_count == 1:
                            print("waiting")
                            print(start_time)
                    
                        if pygame.time.get_ticks() - start_time >= 1000:
                            print(pygame.time.get_ticks())
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            bullet_count = 0
                            freeze_count = 0
                            
                                
                            
                            
                    else:
                        # get current x coord of spaceship
                        bulletX = playerX

                        bullet_sound = mixer.Sound(r"C:\Users\ACER\Desktop\sound\mp3\laser.wav")
                        bullet_sound.play()
                        fire_bullet(bulletX, bulletY)
                        bullet_count += 1
                        print(bullet_count)
                        if bullet_count == 15:
                            freeze()
                        

        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 playerX_change = 0

    playerX += playerX_change

    # checking the boundaries of spaceship
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    # enemy movement

    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            play_again()
            can_bullet_fire = "no"
            bullet_count = 0
            
            break

        
        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            
            

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
           
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            # print(score)
            # create new enemy after it gets killed
            enemyX[i] = random.randint(0,735)  
            enemyY[i] = random.randint(50,120)

        enemy(enemyX[i], enemyY[i], i)      

    # bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    
    if bullet_count == 15:
        rel_font = pygame.font.Font('Starjedi.ttf', 32)
        rel_text = rel_font.render("RELoADiNG...", True, (255,255,0))
        screen.blit(rel_text, (550,12))
        
        
    player(playerX, playerY)
    show_score(textX, textY)
    
    pygame.display.update()
