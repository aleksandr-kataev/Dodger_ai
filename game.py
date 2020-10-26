import pygame
import os
import random
from Player import Player
from Spike import Spike
from Background import Background

# CONSTANS


# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 80)


pygame.init()

PLAYER_RUNNING_IMAGES = [
    pygame.image.load('./img/c1.png'),
    pygame.image.load('./img/c2.png'),
    pygame.image.load('./img/c3.png'),
    pygame.image.load('./img/c4.png'),
    pygame.image.load('./img/c5.png'),
    pygame.image.load('./img/c6.png'),
]

PLAYER_JUMPING_IMAGES = [
    pygame.image.load('./img/j1.png'),
    pygame.image.load('./img/j2.png'),
]


EXPLOSIONS_IMAGES = [
    pygame.image.load('./img/e1.png'),
    pygame.image.load('./img/e2.png'),
    pygame.image.load('./img/e3.png'),
    pygame.image.load('./img/e4.png'),
    pygame.image.load('./img/e5.png'),
    pygame.image.load('./img/e6.png'),
    pygame.image.load('./img/e7.png'),
    pygame.image.load('./img/e8.png'),
    pygame.image.load('./img/e9.png'),
]

SPIKE_IMAGE = pygame.image.load('./img/spike.png')


BACKGROUND_IMAGE = pygame.image.load('./img/background.png')
BACKGROUND_RECT = BACKGROUND_IMAGE.get_rect()
BACKGROUND_SIZE = BACKGROUND_IMAGE.get_size()

FONT_NAME = pygame.font.match_font('arial')

CLOCK = pygame.time.Clock()


ENEMY_PROPB = 100
ENEMIES = []
MIN_TIME_BETWEEN_ENEMIES = 200
CURRENT_TIME_SINCE_LAST_ENEMY = 0


def show_start_screen(screen):
    draw_text(screen, "AI", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Space to jump, avoid enemies",
              22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press any key to begin", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


def show_game_over_screen(screen):
    screen.blit(background, background_rect)
    draw_text(screen, "Game Over", 64, WIDTH/2, HEIGHT/4)
    score_string = "Your score is " + str(player.score)
    draw_text(screen, score_string,
              40, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press any key to try again", 22, WIDTH/2, HEIGHT*3/4)
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
            hits = pygame.sprite.spritecollide(player, enemies, True)
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

    background = Background(BACKGROUND_IMAGE)

    s = Spike(SPIKE_IMAGE)
    all_sprites.add(s)
    enemies.add(s)

    game_over = False
    running = True

    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            initialise_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    player.jump()
                elif event.key == 119:
                    clock_tick += 25
                elif event.key == 115:
                    clock_tick -= 25

        hits = pygame.sprite.spritecollide(player, enemies, True)

        # for hit in hits:
            #enemy_exp_sound.play()
            expl = Explosion(hit.rect.center)
            all_sprites.add(expl)
            game_over = True

        background.update()
        all_sprites.update()
        all_sprites.draw(background.screen)
        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()


run()
