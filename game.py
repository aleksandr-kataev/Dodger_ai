import pygame
import random

# CONSTANS

# Game dimensions
WIDTH = 800
HEIGHT = 800

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 120


class Game()


def centerWindow():
    x = 500
    y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


def initialise_game():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI")
    clock = pygame.time.Clock()

    global all_sprites
    all_sprites = pygame.sprite.Group()

    global enemies
    enemies = pygame.sprite.Group()


def show_start_screen():
    draw_text(window, "AI", 64, WIDTH/2, HEIGHT/4)
    draw_text(window, "Space to jump, avoid enemies",
              22, WIDTH/2, HEIGHT/2)
    draw_text(window, "Press any key to begin", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


def show_game_over_screen():
    window.blit(background, background_rect)
    draw_text(window, "Game Over", 64, WIDTH/2, HEIGHT/4)
    score_string = "Your score is " + str(player.score)
    draw_text(window, score_string,
              40, WIDTH/2, HEIGHT/2)
    draw_text(window, "Press any key to try again", 22, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    pygame.time.delay(2000)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


# Draw lives left
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surface.blit(img, img_rect)


# Draw text, used for the score
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
