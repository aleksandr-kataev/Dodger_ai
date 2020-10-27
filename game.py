import pygame
import os
import random
import neat
import pickle
from Player import Player
from Barrel import Barrel
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

BARREL_IMAGES = [
    pygame.image.load('./img/barrel_1.png'),
    pygame.image.load('./img/barrel_2.png')
]


BACKGROUND_IMAGE = pygame.image.load('./img/background.png')
BACKGROUND_RECT = BACKGROUND_IMAGE.get_rect()
BACKGROUND_SIZE = BACKGROUND_IMAGE.get_size()

FONT_NAME = pygame.font.match_font('arial')

CLOCK = pygame.time.Clock()

BACKGROUND = Background(BACKGROUND_IMAGE)

BARREL_PROB = 100
MIN_TIME_BETWEEN_BARRELS = 80
CURRENT_TIME_SINCE_LAST_BARREL = 0


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

    global barrels
    barrels = pygame.sprite.Group()
    all_sprites.add(barrels)

    if (type != 'ai_train'):
        global player
        player = Player(PLAYER_RUNNING_IMAGES)
        all_sprites.add(player)


def check_barrels(players):
    global CURRENT_TIME_SINCE_LAST_BARREL
    global barrels
    for x, barrel in enumerate(barrels):
        if barrel.rect.right < 0:
            barrel.kill()
            for player in players:
                player.score += 1
    if CURRENT_TIME_SINCE_LAST_BARREL > MIN_TIME_BETWEEN_BARRELS:
        if random.randint(0, BARREL_PROB-1) == 0:
            b = Barrel(BARREL_IMAGES)
            all_sprites.add(b)
            barrels.add(b)
            CURRENT_TIME_SINCE_LAST_BARREL = 0
    else:
        CURRENT_TIME_SINCE_LAST_BARREL += 1


def ai_train_run(genomes, config):
    nets = []
    players = []
    ge = []
    init_sprites('ai_train')
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
        check_barrels(players)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        barrel_index = 0
        if len(players) > 0:
            if len(barrels.sprites()) > 1 and players[0].rect.right > barrels.sprites()[0].rect.left:
                barrel_index = 1

        for x, player in enumerate(players):
            if player.score > 5000:
                game_over = True
                running = False

            ge[x].fitness += 0.1
            if (len(barrels.sprites()) > 0):
                output = nets[x].activate(
                    (player.rect.right, player.rect.top, barrels.sprites()[barrel_index].rect.left, barrels.sprites()[barrel_index].velocity))

                if output[0] > 0:
                    player.jump()

        for x, player in enumerate(players):
            hits = pygame.sprite.spritecollide(
                player, barrels, False, pygame.sprite.collide_mask)
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


def ai_run(genome, config):
    init_sprites('ai_run')
    global player
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    game_over = False
    running = True

    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            init_sprites('ai_run')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        barrel_index = 0

        if len(barrels.sprites()) > 1 and player.rect.right > barrels.sprites()[0].rect.left:
            barrel_index = 1

        if (len(barrels.sprites()) > 0):
            output = net.activate(
                (player.rect.right, player.rect.top, barrels.sprites()[barrel_index].rect.left, barrels.sprites()[barrel_index].velocity))

            if output[0] > 0:
                player.jump()

        hits = pygame.sprite.spritecollide(
            player, barrels, False, pygame.sprite.collide_mask)

        for hit in hits:
            # enemy_exp_sound.play()
            expl = Explosion(hit.rect.center, EXPLOSIONS_IMAGES)
            all_sprites.add(expl)
            game_over = True

        check_barrels([player])
        BACKGROUND.update()
        all_sprites.update()
        all_sprites.draw(BACKGROUND.screen)
        draw_text(BACKGROUND.screen, str(player.score),
                  22, BACKGROUND.size[0] / 2, 10)
        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()


def player_run():
    init_sprites('player_run')
    game_over = False
    running = True

    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            init_sprites('player_run')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    player.jump()

        hits = pygame.sprite.spritecollide(
            player, barrels, False, pygame.sprite.collide_mask)

        for hit in hits:
            # enemy_exp_sound.play()
            expl = Explosion(hit.rect.center, EXPLOSIONS_IMAGES)
            all_sprites.add(expl)
            game_over = True

        check_barrels([player])
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

    best = p.run(ai_train_run, 5)

    pickle.dump(best, open("test_train.pkl", "wb"))


def replay_genome(config_path, genome_path="best.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Call game with only the loaded genome
    ai_run(genome, config)


def start():

    draw_text(BACKGROUND.screen, "AI platformer", 64,
              BACKGROUND.size[0]/2, BACKGROUND.size[1]/4)
    draw_text(BACKGROUND.screen, "Space to jump, avoid barrels",
              22, BACKGROUND.size[0]/2, BACKGROUND.size[1]/2)
    draw_text(BACKGROUND.screen,
              "Press left arrow to play, up arrow to let the ai play or right arrow to train the ai", 18, BACKGROUND.size[0]/2, BACKGROUND.size[1]*3/4)
    pygame.display.flip()
    waiting = True
    mode = 'null'
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mode = 'player'
                    waiting = False
                elif event.key == pygame.K_UP:
                    mode = 'ai_run'
                    waiting = False
                elif event.key == pygame.K_RIGHT:
                    mode = 'ai_train'
                    waiting = False
    if mode == 'player':
        player_run()
    else:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        if mode == 'ai_train':
            run(config_path)
        elif mode == 'ai_run':
            replay_genome(config_path)


if __name__ == "__main__":
    start()
