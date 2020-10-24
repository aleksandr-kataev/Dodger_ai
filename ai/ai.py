
import pygame
import os
import random
import neat
import math
import pickle
from os import path


# Sound effects from:
#   Ted Kerr
#   Gumichan01
#   Duckstruction
#   http://cubeengine.com/forum.php4?action=display_thread&thread_id=2164
#   Jesús Lastra

# Graphics
#   Credit "Kenney.nl" or "www.kenney.nl"


# Center the game window
def centerWindow():
    x = 500
    y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


# Evetn to check if the player is stationary
STILL_DELAY = pygame.USEREVENT+2

img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'img'))
sound_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'sound'))

# Set dimensions
WIDTH = 900
HEIGHT = 900
# Set variables
FPS = 1200
POWERUP_TIME = 5000


# Set colours
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Generation
GEN = 0

# Center the window, initialise pygame and create window
centerWindow()

# Init pygame and pymixer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

# Load images
BACKGROUND_IMAGE = pygame.image.load(
    path.join(img_dir, 'spacebg.jpg')).convert()
BACKGROUND_RECT = BACKGROUND_IMAGE.get_rect()
PLAYER_IMAGE = pygame.image.load(path.join(img_dir, 's0.png')).convert()
PLAYER_IMAGE.set_colorkey(BLACK)
LIVE_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (25, 25))
ASTEROID_IMAGE = pygame.image.load(
    path.join(img_dir, 'asteroid.png')).convert()

# Load player animation
PLAYER_ANIM = {'left': [],
               'right': []
               }
for i in range(6):
    filename = 'l{}.png'.format(i)
    img_left = pygame.image.load(path.join(img_dir, filename)).convert()
    img_left.set_colorkey(BLACK)
    PLAYER_ANIM['left'].append(img_left)
    filename = 'r{}.png'.format(i)
    img_right = pygame.image.load(path.join(img_dir, filename)).convert()
    img_right.set_colorkey(BLACK)
    PLAYER_ANIM['right'].append(img_right)


# Load explosion animation
EXPLOSION_ANIM = {'lg': [],
                  'sm': []}
for i in range(6):
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale((img), (42, 42))
    EXPLOSION_ANIM['lg'].append(img_lg)
    img_sm = pygame.transform.scale((img), (20, 20))
    EXPLOSION_ANIM['sm'].append(img_sm)


# Load sounds
PLAYER_EXP_SOUND = pygame.mixer.Sound(path.join(sound_dir, 'player_exp.wav'))
PLAYER_EXP_SOUND.set_volume(0.0)

BACKGROUND_SOUND = pygame.mixer.music.load(path.join(sound_dir, 'theme.ogg'))
pygame.mixer.music.set_volume(0.0)
pygame.mixer.music.play(loops=-1)


# Spawn asteroid
def spawn_asteroid_enemy(type):
    e = Asteroid(type)
    all_sprites.add(e)
    asteroids.add(e)


# Draw health bar
def draw_health_bar(surface, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = (health/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def draw_gen(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


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


# Random number excluding a certain number, used to generate velocity that is not 0
def range_with_no_number(start, end, exclude):
    l = [i for i in range(start, end) if i != exclude]
    return random.choice(l)


def initialise_game():
    # Ground different sprites together
    global all_sprites
    all_sprites = pygame.sprite.Group()
    global asteroids
    asteroids = pygame.sprite.Group()

    # Spawn 10 enemies initially, 4 of them have to be upgraded enemies
    for i in range(8):
        spawn_asteroid_enemy('reg')

    for i in range(8):
        spawn_asteroid_enemy('left')

    for i in range(8):
        spawn_asteroid_enemy('right')

    pygame.time.set_timer(STILL_DELAY, 3000)


def show_start_screen():
    draw_text(window, "ShuttleBattle", 64, WIDTH/2, HEIGHT/4)
    draw_text(window, "Arrow keys to move, space to shoot",
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
    window.blit(BACKGROUND_IMAGE, BACKGROUND_RECT)
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

# Player class


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PLAYER_IMAGE
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 32
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.velocity = 5
        self.fly_count = 0
        self.right = False
        self.left = False
        self.health = 100
        self.score_update = pygame.time.get_ticks()
        self.lives = 1
        self.hidden = False
        self.score = 0
        self.isAlive = True
        self.previousx = self.rect.centerx
        self.invincible = False
        self.invincible_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.isAlive = True

        if self.invincible and pygame.time.get_ticks() - self.invincible > 2500:
            self.invincible = False

        if pygame.time.get_ticks() - self.score_update > 100:
            if self.isAlive:
                self.score_update = pygame.time.get_ticks()
                self.score += 10

        keystate = pygame.key.get_pressed()

        if self.rect.left > 0 and self.left:
            self.rect.x -= self.velocity
        elif self.rect.right < WIDTH and self.right:
            self.rect.x += self.velocity
        else:
            self.left = False
            self.right = False
            self.fly_count = 0

        if self.fly_count + 1 > 18:
            self.fly_count = 17

        if self.fly_count - 1 < -18:
            self.fly_count = -17

        if self.left and self.fly_count <= 0:
            self.image = PLAYER_ANIM['left'][abs(self.fly_count) // 3]
            self.fly_count -= 1
        elif self.left and self.fly_count > 0:
            self.image = PLAYER_ANIM['right'][self.fly_count // 3]
            self.fly_count -= 1
        elif self.right and self.fly_count >= 0:
            self.image = PLAYER_ANIM['right'][self.fly_count // 3]
            self.fly_count += 1
        elif self.right and self.fly_count < 0:
            self.image = PLAYER_ANIM['left'][abs(self.fly_count) // 3]
            self.fly_count += 1
        else:
            self.image = PLAYER_IMAGE

    def make_invincible(self):
        self.invincible = True
        self.invincible = pygame.time.get_ticks()

    def hide(self):
        # hide the player when dead
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH + 500, HEIGHT + 200)
        self.make_invincible()

    def dead(self, hit):
        self.isAlive = False
        self.player_death_expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(self.player_death_expl)
        self.hide()
        self.lives -= 1
        self.health = 100

    def isHit(self, hit):
        self.health -= 35
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)


# Asteroid class


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, type):
        self.image = ASTEROID_IMAGE
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.type = type
        if (self.type == 'reg'):
            self.rect.x = random.randrange(
                self.rect.width, WIDTH - self.rect.width)
        elif (self.type == 'left'):
            self.rect.x = 0
        elif (self.type == 'right'):
            self.rect.x = WIDTH - self.rect.width

        self.rect.y = random.randrange(-20, 0)
        self.radius = 20
        self.image.set_colorkey(BLACK)
        self.firerate = 5
        self.y_velocity = random.randrange(2, 4)

    def update(self):
        self.rect.y += self.y_velocity

        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.y = random.randrange(-20, 0)
            if (self.type == 'reg'):
                self.rect.x = random.randrange(
                    self.rect.width, WIDTH - self.rect.width)
            elif (self.type == 'left'):
                self.rect.x = 0
            elif (self.type == 'right'):
                self.rect.x = WIDTH - self.rect.width


# Explosion class


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = EXPLOSION_ANIM[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 25

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(EXPLOSION_ANIM[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = EXPLOSION_ANIM[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def asteroidPos():
    pos = []
    for asteroid in asteroids:
        if asteroid.type == 'reg':
            pos.append(asteroid.rect.x)
            pos.append(asteroid.rect.y)
    return pos


def eval_genomes(genomes, config):
    global GEN
    GEN += 1

    players = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player())
        g.fitness = 0
        ge.append(g)

    # show_start_screen()
    initialise_game()
    for player in players:
        all_sprites.add(player)
    game_over = False
    running = True
    # Loop
    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            initialise_game()
        clock.tick(FPS)

        if len(players) < 1:
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            # elif event.type == STILL_DELAY:
            #    for x, player in enumerate(players):
            #        if player.rect.centerx == player.previousx:
            #            ge[x].fitness -= 60
            #            player.dead(player)
            #        player.previousx = player.rect.centerx

        # Update sprites
        all_sprites.update()

        for x, player in enumerate(players):
            if not player.invincible:

                if player.isAlive:
                    ge[x].fitness += 0.025

                hits = pygame.sprite.spritecollide(
                    player, asteroids, True, pygame.sprite.collide_circle)
                for hit in hits:
                    PLAYER_EXP_SOUND.play()
                    player.isHit(hit)
                    if player.health <= 0:
                        player.dead(hit)
                    else:
                        ge[x].fitness -= 20

                    if (hit.type == 'reg'):
                        spawn_asteroid_enemy('reg')
                    elif (hit.type == 'left'):
                        spawn_asteroid_enemy('left')
                    else:
                        spawn_asteroid_enemy('right')

                if player.lives < 1 and not player.player_death_expl.alive():
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    player.kill()

        # move player
        for x, player in enumerate(players):
            dist = asteroidPos()

            output = nets[x].activate((
                player.rect.centerx,
                dist[0],
                dist[1],
                dist[2],
                dist[3],
                dist[4],
                dist[5],
                dist[6],
                dist[7],
                dist[8],
                dist[9],
                dist[10],
                dist[11],
                dist[12],
                dist[13],
                dist[14],
                dist[15],
            ))

            # print(output[0])

            if output[0] < 0:
                player.left = True
                player.right = False

            elif output[0] > 0:
                player.left = False
                player.right = True

            if player.score > 100000:
                print('achived score')
                break

        # Render
        window.fill(BLACK)
        window.blit(BACKGROUND_IMAGE, BACKGROUND_RECT)
        all_sprites.draw(window)
        draw_text(window, str(player.score), 22, WIDTH / 2, 10)
        draw_gen(window, "Generation: " + str(GEN), 22, 60, 9)
        draw_health_bar(window, WIDTH-205, 5, player.health)
        draw_lives(window, WIDTH-205, 40, player.lives, LIVE_IMAGE)
        pygame.display.flip()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('didnt not acheve score')

    model = open('ai_model.pickle', 'wb')
    pickle.dump(winner, model)
    model.close()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
