import pygame
import random
import math
import sys
import time
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 700))

# Colors
green = (0, 255, 0)
yellow = (255, 255, 0)

# Window title and icon
pygame.display.set_caption("Rocket Run")
window_icon = pygame.image.load("images/rocket.png")
pygame.display.set_icon(window_icon)

# Main menu background images and font
menu_background_image = pygame.image.load("images/menu_background.jpg")
menu_rocket_image = pygame.image.load("images/menu_rocket.png")
menu_title = pygame.font.SysFont("comicsans", 120, bold=True).render("ROCKET RUN", True, (255, 60, 60))

# Main menu arrow key images
arrow_keys_image = pygame.image.load("images/arrow_keys.png")
left_arrow_key_image = pygame.image.load("images/left_arrow_key.png")
right_arrow_key_image = pygame.image.load("images/right_arrow_key.png")

# Main menu easy/medium/hard
easy_button = pygame.Rect(150, 550, 150, 50)
easy_text = pygame.font.SysFont("timesnewroman", 30, bold=True).render("EASY", True, yellow)
medium_button = pygame.Rect(350, 550, 150, 50)
medium_text = pygame.font.SysFont("timesnewroman", 30, bold=True).render("MEDIUM", True, yellow)
hard_button = pygame.Rect(550, 550, 150, 50)
hard_text = pygame.font.SysFont("timesnewroman", 30, bold=True).render("HARD", True, yellow)

# Main menu instructions
first_instruction_text = pygame.font.SysFont("comicsans", 35, bold=False).render("Use arrow keys to dodge the meteors", True, yellow)
second_instruction_text = pygame.font.SysFont("comicsans", 35, bold=False).render("Left arrow key moves rocket to the left", True, yellow)
third_instruction_text = pygame.font.SysFont("comicsans", 35, bold=False).render("Right arrow key moves rocket to the right", True, yellow)

# Background image when playing the game
background_image = pygame.image.load("images/rocket_run_background.jpg")

# To override countdown number when it reaches 0
override_image = pygame.image.load("images/rocket_run_background_countdown_blit_override.jpg")

# Variables to give background a scrolling effect
background_y = 0
background_height = background_image.get_rect().height

# Game song
mixer.music.load("sounds/rocket_run_song.wav")
mixer.music.play(-1)

# Player
player_image = pygame.image.load("images/player_rocket.png")
player_x = 415
player_y = 470
player_x_change = 0

# Meteor
meteor_image = pygame.image.load("images/meteor.png")
meteors = []
meteor_x = []
meteor_y = []
meteor_y_change = []
num_of_meteors = 13

for i in range(num_of_meteors):
    meteors.append(meteor_image)
    meteor_x.append(random.randint(0, 836))
    meteor_y.append(random.randint(-300, -50))

# Score
score_value = 0
score_text_x = 10
score_text_y = 10

# For countdown
start_time = 4
countdown_font = pygame.font.SysFont("timesnewroman", 64, bold=True)
countdown = True

# For game over
explosion_sound = mixer.Sound("sounds/explosion.wav")
rocket_explosion_image = pygame.image.load("images/rocket_explosion.png")
game_over_text = pygame.font.Font("freesansbold.ttf", 64).render("GAME OVER", True, green)
retry_button = pygame.Rect(370, 320, 150, 50)
retry_button_text = pygame.font.SysFont("timesnewroman", 30, bold=True).render("RETRY", True, (170, 250, 170))

# Must declare for later functionality
menu = True
retry = False


def player(x, y):
    screen.blit(player_image, (x, y))


def meteor(x, y, i):
    screen.blit(meteors[i], (x, y))


def display_game_over():
    screen.blit(game_over_text, (240, 230))


def display_score(x, y):
    score_text = pygame.font.Font("freesansbold.ttf", 32).render("SCORE: " + str(score_value), True, green)
    screen.blit(score_text, (x, y))


def easy_medium_hard_text():
    screen.blit(easy_text, (185, 560))
    screen.blit(medium_text, (358, 560))
    screen.blit(hard_text, (581, 560))


def arrow_keys():
    screen.blit(arrow_keys_image, (27, 150))
    screen.blit(left_arrow_key_image, (70, 310))
    screen.blit(right_arrow_key_image, (70, 420))


def instructions():
    screen.blit(first_instruction_text, (167, 205))
    screen.blit(second_instruction_text, (120, 320))
    screen.blit(third_instruction_text, (120, 430))


def collision_checker(meteor_x, meteor_y, player_x, player_y):
    collision_check = math.sqrt((math.pow(meteor_x - player_x, 2)) + (math.pow(meteor_y - player_y, 2)))
    if collision_check < 45:
        return True
    else:
        return False


def main_menu():
    global menu, meteor_y_change

    while menu:
        screen.blit(menu_background_image, (0, 0))
        screen.blit(menu_title, (125, 50))
        screen.blit(menu_rocket_image, (560, 160))
        arrow_keys()
        instructions()

        x, y = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (255, 60, 60), easy_button, 7)
        pygame.draw.rect(screen, (255, 60, 60), medium_button, 7)
        pygame.draw.rect(screen, (255, 60, 60), hard_button, 7)

        easy_medium_hard_text()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteor_y_change.append(3.5)
                        menu = False
                elif medium_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteor_y_change.append(5)
                        menu = False
                elif hard_button.collidepoint(x, y):
                    if event.button == 1:
                        for i in range(num_of_meteors):
                            meteor_y_change.append(7)
                        menu = False

        pygame.display.update()


def countdown_display():
    global countdown_font, countdown, start_time

    while countdown:

        screen.blit(background_image, (0, 0))

        player(player_x, player_y)

        for k in range(0, 4):
            start_time -= 1
            if start_time == 0:
                time.sleep(0.7)
                screen.blit(override_image, (352, 215))
                screen.blit(countdown_font.render("BLAST OFF!", True, green), (265, 315))
                pygame.display.update()
                time.sleep(0.7)
                countdown = False
                pygame.display.update()
            else:
                screen.blit(override_image, (352, 215))
                countdown_text = countdown_font.render(str(start_time), True, green)
                screen.blit(countdown_text, (430, 315))
                time.sleep(0.7)
                pygame.display.update()


def display_retry():
    global retry, player_x, player_y, menu, countdown

    screen.blit(background_image, (0, 0))
    screen.blit(rocket_explosion_image, (player_x - 85, player_y - 85))
    display_score(score_text_x, score_text_y)
    display_game_over()
    player_y = 5000

    pygame.draw.rect(screen, (255, 60, 60), retry_button, 7)
    screen.blit(retry_button_text, (393, 328))

    while not retry:
        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(x, y):
                    if event.button == 1:
                        reinitialize()
                        menu = True
                        countdown = True
                        main()
                        retry = True

        pygame.display.update()


def reinitialize():
    global player_x, player_y, player_x_change, meteors, meteor_x, meteor_y, meteor_y_change, score_value, \
            background_y, start_time

    player_x = 415
    player_y = 470
    player_x_change = 0
    meteors = []
    meteor_x = []
    meteor_y = []
    meteor_y_change = []
    score_value = 0
    background_y = 0
    start_time = 4

    for i in range(num_of_meteors):
        meteors.append(meteor_image)
        meteor_x.append(random.randint(0, 836))
        meteor_y.append(random.randint(-300, -50))


def main():
    global background_y, player_x, player_y, meteor_x, meteor_y, player_x_change, meteor_y_change, score_value

    running = True

    while running:

        main_menu()

        if not menu:
            countdown_display()

        background_y_rel = background_y % background_height
        screen.blit(background_image, (0, background_y_rel - background_height))

        if background_y_rel < background_height:
            screen.blit(background_image, (0, background_y_rel))

        background_y += 2.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change += -6
                elif event.key == pygame.K_RIGHT:
                    player_x_change += 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        player_x += player_x_change

        if player_x >= 836:
            player_x = 836
        elif player_x <= 0:
            player_x = 0

        for i in range(num_of_meteors):

            score_value += 1

            collision = collision_checker(meteor_x[i], meteor_y[i], player_x, player_y)

            if collision:
                explosion_sound.play()
                display_retry()

            if meteor_y[i] >= 636:
                meteor_x[i] = random.randint(0, 836)
                meteor_y[i] = random.randint(-300, -50)

            meteor_y[i] += meteor_y_change[i]
            meteor(meteor_x[i], meteor_y[i], i)

        player(player_x, player_y)
        display_score(score_text_x, score_text_y)

        pygame.display.update()


main()
