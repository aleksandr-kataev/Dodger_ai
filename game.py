import pygame
import os
import random
from Player import Player

# CONSTANS

# Game dimensions
WIDTH = 1436
HEIGHT = 923

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 30


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 80)


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI")

PLAYER_RUNNING_IMAGES = [
    pygame.image.load('./img/c1.png'),
    pygame.image.load('./img/c2.png'),
    pygame.image.load('./img/c3.png'),
    pygame.image.load('./img/c4.png'),
    pygame.image.load('./img/c5.png'),
    pygame.image.load('./img/c6.png'),
]

PLAYER_JUMPING_IMAGES = [
    pygame.image.load('./img/j1.png').convert(),
    pygame.image.load('./img/j2.png').convert(),
]


EXPLOSIONS_IMAGES = [
    pygame.image.load('./img/e1.png').convert(),
    pygame.image.load('./img/e2.png').convert(),
    pygame.image.load('./img/e3.png').convert(),
    pygame.image.load('./img/e4.png').convert(),
    pygame.image.load('./img/e5.png').convert(),
    pygame.image.load('./img/e6.png').convert(),
    pygame.image.load('./img/e7.png').convert(),
    pygame.image.load('./img/e8.png').convert(),
    pygame.image.load('./img/e9.png').convert(),
]

ENEMIES_IMAGES = [
    pygame.image.load('./img/spike.png').convert(),
]

BACKGROUND_IMAGE = pygame.image.load('./img/background.png').convert()
BACKGROUND_RECT = BACKGROUND_IMAGE.get_rect()

FONT_NAME = pygame.font.match_font('arial')

CLOCK = pygame.time.Clock()

ENEMY_PROPB = 100
ENEMIES = []
MIN_TIME_BETWEEN_ENEMIES = 200
CURRENT_TIME_SINCE_LAST_ENEMY = 0


def show_start_screen():
    draw_text(window, "AI", 64, WIDTH/2, HEIGHT/4)
    draw_text(window, "Space to jump, avoid enemies",
              22, WIDTH/2, HEIGHT/2)
    draw_text(window, "Press any key to begin", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        CLOCK.tick(FPS)
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
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def init_sprites(type):
    # Ground different sprites together
    global all_sprites
    all_sprites = pygame.sprite.Group()

    global enemies
    enemies = pygame.sprite.Group()
    all_sprites.add(enemies)

    if (type != 'controlled'):
        global player
        player = Player(PLAYER_RUNNING_IMAGES)
        all_sprites.add(player)


def controlled_run():
    players = []

    # Ground different sprites together
    global all_sprites
    all_sprites = pygame.sprite.Group()
    global enemies
    enemies = pygame.sprite.Group()

    running = True

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        for x, player in enumerate(players):
            hits = pygame.sprite.groupcollide(enemies, player, True, True)
            for hit in hits:
                # enemy_exp_sound.play()
                # TODO explosion class
                expl = Explosion(hit.rect.center)
                all_sprites.add(expl)
                game_over = True

        window.fill(BLACK)
        window.blit(BACKGROUND_IMAGE, BACKGROUND_RECT)
        all_sprites.draw(window)
        pygame.display.flip()

    pygame.quit()
    quit()


def run():
    # show_start_screen()

    init_sprites('run')

    game_over = False
    running = True

    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            initialise_game()

        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, player, True, True)

        for hit in hits:
            # enemy_exp_sound.play()
            expl = Explosion(hit.rect.center)
            all_sprites.add(expl)
            game_over = True

        window.fill(WHITE)
        window.blit(BACKGROUND_IMAGE, BACKGROUND_RECT)
        all_sprites.draw(window)
        pygame.display.flip()

    pygame.quit()
    quit()


run()
