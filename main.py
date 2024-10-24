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
score_font = pygame.font.Font(None, 100)
menu_text_font = pygame.font.Font(None, 50)
velo = 10
player_1_score = 0
player_2_score = 0
click = False
last_scored = None

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
ball_rect.x = screen.get_width() / 2
ball_rect.y = screen.height / 10
player1_rect = player1.get_rect()
player1_rect.x = 100
player1_rect.y = 310
player2_rect = player2.get_rect()
player2_rect.x = 980
player2_rect.y = 310

# Vectors
ball_position = pygame.Vector2(ball_rect.topleft)
ball_velocity = pygame.Vector2(10, 10)


# Functions
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


def handle_ball_movement(ball_moving):

    if ball_moving:
        ball_position.x += ball_velocity.x
        ball_position.y += ball_velocity.y
        ball_rect.topleft = (ball_position.x, ball_position.y)


# Modify handle_scoring function to update last_scored
def handle_scoring(ball_moving, player_1_score, player_2_score):
    global last_scored
    global last_scored  # Reference the global variable

    if ball_position.x > screen.get_width() or ball_position.x < 0:
        if ball_position.x > screen.get_width():
            player_1_score += 1
            last_scored = "player2"  # Player 2 scored on Player 1
        else:  # ball_position.x < 0:
            player_2_score += 1
            last_scored = "player1"  # Player 1 scored on Player 2

        ball_moving = False
        ball_position.x = screen.get_width() / 2
        ball_position.y = screen.get_height() / 10
        ball_rect.topleft = (ball_position.x, ball_position.y)

        # Serve the ball to the player who was last scored on

        if last_scored == "player1":
            ball_velocity.x = -abs(ball_velocity.x)
        else:
            ball_velocity.x = abs(ball_velocity.x)

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


def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


def end_game_menu(winner):
    click = False
    while True:
        screen.fill((0, 0, 0))

        # Center the title text
        title_text = f"{winner} won! Would you like to continue?"
        title_surface = menu_text_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surface, title_rect)

        mx, my = pygame.mouse.get_pos()

        # Button dimensions
        button_width, button_height = 75, 75

        # Calculate button positions based on screen width and button width
        button_1_x = (screen.get_width() // 2) - (
            button_width + 20
        )  # Left button with some spacing
        button_2_x = (screen.get_width() // 2) + 20  # Right button with some spacing

        # Button rectangles
        button_1 = pygame.Rect(button_1_x, 360, button_width, button_height)
        button_2 = pygame.Rect(button_2_x, 360, button_width, button_height)

        # Draw buttons
        pygame.draw.rect(screen, (255, 255, 255), button_1)
        pygame.draw.rect(screen, (255, 255, 255), button_2)

        # Center text within buttons
        yes_surface = menu_text_font.render("Yes", True, (0, 0, 0))
        no_surface = menu_text_font.render("No", True, (0, 0, 0))

        yes_rect = yes_surface.get_rect(center=button_1.center)
        no_rect = no_surface.get_rect(center=button_2.center)

        screen.blit(yes_surface, yes_rect)
        screen.blit(no_surface, no_rect)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx, my)) and click:
            # Restart the game logic or reset variables as needed
            game(
                running, False, player_1_score, player_2_score
            )  # Reset scores as needed
            return  # Exit the menu after starting the game

        if button_2.collidepoint((mx, my)) and click:
            pygame.quit()
            return  # Exit the menu

        pygame.display.flip()
        clock.tick(60)


def game(running, ball_moving, player_1_score, player_2_score):
    while running:
        # click = False

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.KEYDOWN:
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

        handle_ball_movement(ball_moving)
        ball_moving, player_1_score, player_2_score = handle_scoring(
            ball_moving,
            player_1_score,
            player_2_score,
        )
        handle_wall_bouncing()
        handle_paddle_bouncing()

        # Inside your main loop

        draw_text(
            str(player_1_score),
            score_font,
            (255, 255, 255),
            screen,
            270,
            20,
        )

        draw_text(
            str(player_2_score),
            score_font,
            (255, 255, 255),
            screen,
            810,
            20,
        )
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60


game(running, ball_moving, player_1_score, player_2_score)
pygame.quit()
