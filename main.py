import pygame
from pygame.locals import *
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
running = True
ball_moving = False

velo = 10

player_1_score = 0
player_2_score = 0

# Surfaces
player1 = pygame.Surface((10, 100))
player1.fill("white")
player2 = pygame.Surface((10, 100))
player2.fill("white")
boarder = pygame.Surface((10, round(math.sqrt(720))))
boarder.fill("white")
ball = pygame.Surface((10, 10))
ball.fill("white")

# Rects
ball_rect = ball.get_rect()
ball_rect.x = 3 / 8 * screen.width
ball_rect.y = screen.height / 2
player1_rect = player1.get_rect()
player1_rect.x = 100
player1_rect.y = 310
player2_rect = player2.get_rect()
player2_rect.x = 980
player2_rect.y = 310

# Vectors
ball_position = pygame.Vector2(ball_rect.topleft)
ball_velocity = pygame.Vector2(10, 10)


def player1_handle_movement(keys_pressed, player_rect):

    if keys_pressed[K_w] and player_rect.y - velo >= 0:  # UP
        player_rect.y -= velo
    if (
        keys_pressed[K_s] and player_rect.y + velo + player_rect.height <= screen.height
    ):  # DOWN
        player_rect.y += velo


def player2_handle_movement(keys_pressed, player_rect):

    if keys_pressed[K_o] and player_rect.y - velo >= 0:  # UP
        player_rect.y -= velo
    if (
        keys_pressed[K_l] and player_rect.y + velo + player_rect.height <= screen.height
    ):  # DOWN
        player_rect.y += velo


# Initial movement
def handle_ball_movement(ball_moving):

    if ball_moving:
        ball_position.x += ball_velocity.x
        ball_position.y += ball_velocity.y
        ball_rect.topleft = (ball_position.x, ball_position.y)


def handle_scoring(ball_moving, player_1_score, player_2_score):

    if ball_position.x > screen.get_width() or ball_position.x < 0:
        if ball_position.x > screen.get_width():
            player_1_score += 1
            print("player 1 scored!", player_1_score)
        else:  # ball_position.x < 0:
            player_2_score += 1
            print("player 2 scored!", player_2_score)

        ball_moving = False
        ball_position.x = 3 / 8 * screen.get_width()
        ball_position.y = screen.get_height() / 2
        ball_rect.topleft = (ball_position.x, ball_position.y)

    return ball_moving, player_1_score, player_2_score


def handle_wall_bouncing():

    if ball_position.y > screen.height or ball_position.y < 0:
        if ball_position.y > screen.height:
            normal = pygame.Vector2(0, -1)
        else:
            normal = pygame.Vector2(0, 1)
        ball_velocity.reflect_ip(normal)
        ball_rect.topleft = (ball_position.x, ball_position.y)


def handle_paddle_bouncing():

    if ball_rect.colliderect(player1_rect):
        ball_velocity.x = abs(ball_velocity.x)  # Move right
        ball_position.x = player1_rect.right  # Place the ball just off the paddle
    elif ball_rect.colliderect(player2_rect):
        ball_velocity.x = -abs(ball_velocity.x)  # Move left
        ball_position.x = player2_rect.left - ball_rect.width
        ball_rect.topleft = (ball_position.x, ball_position.y)


while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                ball_moving = True

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    screen.blit(player1, (100, player1_rect.y))
    screen.blit(player2, (980, player2_rect.y))
    screen.blit(ball, (ball_rect.x, ball_rect.y))

    for i in range(0, screen.height, 50):
        screen.blit(boarder, (screen.width / 2, i))

    keys_pressed = pygame.key.get_pressed()
    player1_handle_movement(keys_pressed, player1_rect)
    player2_handle_movement(keys_pressed, player2_rect)
    # ball_moving = update_ball(ball_position, ball_moving)

    handle_ball_movement(ball_moving)
    ball_moving, player_1_score, player_2_score = handle_scoring(
        ball_moving, player_1_score, player_2_score
    )
    handle_wall_bouncing()
    handle_paddle_bouncing()

    # flip() the display to put your work on screen
    pygame.display.flip()
    # print(ball_rect.topleft, ball_position, ball_moving)

    clock.tick(60)  # limits FPS to 60

pygame.quit()
