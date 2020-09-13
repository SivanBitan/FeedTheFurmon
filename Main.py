import math
import random
import pygame
from pygame import mixer


# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Feed The Furmon")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Furmon
furmonImg = []
furmonX = []
furmonY = []
furmonX_change = []
furmonY_change = []
num_of_furmons = 9

# Add furmons to screen
for i in range(num_of_furmons):
    furmonImg.append(pygame.image.load('furmon.png'))
    furmonX.append(random.randint(0, 736))
    furmonY.append(random.randint(50, 150))
    furmonX_change.append(4)
    furmonY_change.append(40)

# Pepper

# Ready - The player can't see the pepper on the screen
# Shoot - The pepper is currently moving

pepperImg = pygame.image.load('pepper.png')
pepperX = 0
pepperY = 480
pepperX_change = 0
pepperY_change = 20
pepper_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('BAUHS93.ttf', 32)
textX = 10
testY = 10

# Game Over

over_font = pygame.font.Font('BAUHS93.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    over_text = font.render("Press SPACE for a new game or ESC to quit.", True, (255, 255, 255))
    screen.blit(over_text, (70, 400))


def player(x, y):
    screen.blit(playerImg, (x, y))


def furmon(x, y, i):
    screen.blit(furmonImg[i], (x, y))


def shoot_pepper(x, y):
    global pepper_state
    pepper_state = "shoot"
    screen.blit(pepperImg, (x + 16, y + 10))


def isCollision(furmonX, furmonY, pepperX, pepperY):
    # Furmon meeting pepper
    distance = math.sqrt(math.pow(furmonX - pepperX, 2) + (math.pow(furmonY - pepperY, 2)))
    if distance < 27:
        return True
    else:
        return False

def isPlayerCollision(furmonX, furmonY,playerX, playerY):
    # Player meeting furmon
    Any_playerX = playerX
    Any_playerY = playerY
    for index in range(6):
        distance = math.sqrt(math.pow(furmonX[index] - Any_playerX, 2) + (math.pow(furmonY[index] - Any_playerY, 2)))
        if distance <= 30:
            return True
    return False



# Game Loop

running = True
while running:

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # Sniff events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if any key in the keyboard is pressed check whether its right or left, up or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_UP:
                playerY_change = -10
            if event.key == pygame.K_DOWN:
                playerY_change = 10

        # if the pressed key is space the player meant to shoot
            if event.key == pygame.K_SPACE:
                if pepper_state is "ready":
                    pepperSound = mixer.Sound("pepperShot.wav")
                    pepperSound.play()
                    # Get the current cordinates of the spaceship
                    pepperX = playerX
                    pepperY = playerY
                    shoot_pepper(pepperX, pepperY)
            if event.key == pygame.K_p:
                pygame.display.toggle_fullscreen
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Left to right boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Up and down boundaries
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Furmon Movement
    isExplosion = isPlayerCollision(furmonX, furmonY, playerX, playerY)  # check if a collision happened
    # Loop of furmons
    for i in range(num_of_furmons):

        # Game Over

        if furmonY[i] > 440 or isExplosion:

            for j in range(num_of_furmons):
                furmonY[j] = 2000

            if isExplosion:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()

            game_over_text()
            playerImg = pygame.image.load('collision.png')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # RE-INITIALLIZE GAME
                    screen = pygame.display.set_mode((800, 600))
                    # Background
                    background = pygame.image.load('background.png')
                    # Sound
                    mixer.music.load("background.wav")
                    mixer.music.play(-1)
                    # Player
                    playerImg = pygame.image.load('player.png')
                    playerX = 370
                    playerY = 480
                    playerX_change = 0
                    playerY_change = 0
                    # Furmons
                    furmonImg = []
                    furmonX = []
                    furmonY = []
                    furmonX_change = []
                    furmonY_change = []
                    num_of_furmons = 9
                    for i in range(num_of_furmons):
                        furmonImg.append(pygame.image.load('furmon.png'))
                        furmonX.append(random.randint(0, 736))
                        furmonY.append(random.randint(50, 150))
                        furmonX_change.append(4)
                        furmonY_change.append(40)
                    # Pepper
                    pepperImg = pygame.image.load('pepper.png')
                    pepperX = 0
                    pepperY = playerY
                    pepperX_change = 0
                    pepperY_change = 20
                    pepper_state = "ready"
                    # Score
                    score_value = 0

                if event.key == pygame.K_ESCAPE:
                    # QUIT GAME + CLOSE WINDOW AND PROGRAM
                    pygame.quit()
                    exit(0)

        # Change in placement for furmons
        furmonX[i] += furmonX_change[i]
        if furmonX[i] <= 0:
            furmonX_change[i] = 4
            furmonY[i] += furmonY_change[i]
        elif furmonX[i] >= 736:
            furmonX_change[i] = -4
            furmonY[i] += furmonY_change[i]

        # Eating pepper
        eating = isCollision(furmonX[i], furmonY[i], pepperX, pepperY)
        if eating:
            eatingSound = mixer.Sound("eat.wav")
            eatingSound.play()
            pepperY = playerY
            pepper_state = "ready"
            score_value += 1
            furmonX[i] = random.randint(0, 736)
            furmonY[i] = random.randint(50, 150)

        furmon(furmonX[i], furmonY[i], i)

    # Pepper Movement
    if pepperY <= 0:
        pepperY = playerY
        pepper_state = "ready"

    if pepper_state is "shoot":
        shoot_pepper(pepperX, pepperY)
        pepperY -= pepperY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
