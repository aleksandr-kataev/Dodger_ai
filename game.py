import pygame
import os
import random
import neat
from Player import Player
from Spike import Spike
from Background import Background
from Explosion import Explosion

# CONSTANS


# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 120

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

BACKGROUND = Background(BACKGROUND_IMAGE)

ENEMY_PROPB = 100
MIN_TIME_BETWEEN_ENEMIES = 100
CURRENT_TIME_SINCE_LAST_ENEMY = 0


def show_game_over_screen():
    draw_text(BACKGROUND.screen, "Game Over", 64,
              BACKGROUND.size[0]/2, BACKGROUND.size[1]/4)
    score_string = "Your score is " + str(player.score)
    draw_text(BACKGROUND.screen, score_string,
              40, BACKGROUND.size[0]/2, BACKGROUND.size[1]/2)
    draw_text(BACKGROUND.screen, "Press any key to try again",
              22, BACKGROUND.size[0]/2, BACKGROUND.size[1]*3/4)
    pygame.display.flip()
    pygame.time.delay(2000)
    waiting = True
    while waiting:
        CLOCK.tick(FPS)
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

    if (type != 'ai'):
        global player
        player = Player(PLAYER_RUNNING_IMAGES)
        all_sprites.add(player)


def check_enemy():
    global CURRENT_TIME_SINCE_LAST_ENEMY
    global enemies
    for x, enemy in enumerate(enemies):
        if enemy.rect.right < 0:
            enemy.kill()
    if CURRENT_TIME_SINCE_LAST_ENEMY > MIN_TIME_BETWEEN_ENEMIES:
        if random.randint(0, ENEMY_PROPB-1) == 0:
            s = Spike(SPIKE_IMAGE)
            all_sprites.add(s)
            enemies.add(s)
            CURRENT_TIME_SINCE_LAST_ENEMY = 0
    else:
        CURRENT_TIME_SINCE_LAST_ENEMY += 1


def ai_run(genomes, config):
    gen = 0
    nets = []
    players = []
    ge = []
    init_sprites('ai')
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        player = Player(PLAYER_RUNNING_IMAGES)
        global all_sprites
        all_sprites.add(player)
        players.append(player)
        ge.append(genome)

    game_over = False
    running = True

    while running and len(players) > 0:
        CLOCK.tick(FPS)
        check_enemy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        spike_index = 0
        if len(players) > 0:
            if len(enemies.sprites()) > 1 and players[0].rect.right > enemies.sprites()[0].rect.left:
                spike_index = 1

        for x, player in enumerate(players):
            ge[x].fitness += 0.1
            if (len(enemies.sprites()) > 0):
                output = nets[x].activate(
                    (player.rect.top, enemies.sprites()[spike_index].rect.left, enemies.sprites()[spike_index].velocity))

                if output[0] > 0:
                    player.jump()

        for x, player in enumerate(players):
            hits = pygame.sprite.spritecollide(
                player, enemies, False, pygame.sprite.collide_mask)
            for hit in hits:
                # enemy_exp_sound.play()
                expl = Explosion(hit.rect.center, EXPLOSIONS_IMAGES)
                all_sprites.add(expl)
                ge[x].fitness -= 1
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
                player.kill()

        BACKGROUND.update()
        all_sprites.update()
        all_sprites.draw(BACKGROUND.screen)
        draw_text(BACKGROUND.screen, str(player.score),
                  22, BACKGROUND.size[0] / 2, 10)
        pygame.display.flip()
        CLOCK.tick(FPS)


def player_run():

    init_sprites('run')

    game_over = False
    running = True

    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            init_sprites('run')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    player.jump()

        hits = pygame.sprite.spritecollide(
            player, enemies, False, pygame.sprite.collide_mask)

        for hit in hits:
            # enemy_exp_sound.play()
            expl = Explosion(hit.rect.center, EXPLOSIONS_IMAGES)
            all_sprites.add(expl)
            game_over = True

        check_enemy()
        BACKGROUND.update()
        all_sprites.update()
        all_sprites.draw(BACKGROUND.screen)
        draw_text(BACKGROUND.screen, str(player.score),
                  22, BACKGROUND.size[0] / 2, 10)
        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(ai_run, 50)


def start():

    draw_text(BACKGROUND.screen, "AI platformer", 64,
              BACKGROUND.size[0]/2, BACKGROUND.size[1]/4)
    draw_text(BACKGROUND.screen, "Space to jump, avoid enemies",
              22, BACKGROUND.size[0]/2, BACKGROUND.size[1]/2)
    draw_text(BACKGROUND.screen,
              "Press right arrow to play or left arrow to ley the ai play", 18, BACKGROUND.size[0]/2, BACKGROUND.size[1]*3/4)
    pygame.display.flip()
    waiting = True
    mode = 'null'
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mode = 'p'
                    waiting = False
                elif event.key == pygame.K_LEFT:
                    mode = 'a'
                    waiting = False

    if mode == 'a':
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        run(config_path)
    elif mode == 'p':
        player_run()


if __name__ == "__main__":
    start()


# TODO
# explosion animation larger
# different sprite for enemy
# score based on enemy passed rather than time
