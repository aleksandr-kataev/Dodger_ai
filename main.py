import pygame
import os
import random
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


img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')

# Set dimensions
WIDTH = 900
HEIGHT = 900
# Set variables
FPS = 120
POWERUP_TIME = 5000


# Set colours
GREEN = (0,255,0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Center the window, initialise pygame and create window
centerWindow()

#Init pygame and pymixer
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


# Spawn asteroid
def spawn_asteroid_enemy():
    e = Asteroid()
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
    global player
    player = Player()
    all_sprites.add(player)

    # Spawn 10 enemies initially, 4 of them have to be upgraded enemies
    for i in range(8):
        spawn_asteroid_enemy()


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

# Player class


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
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
        self.shoot_delay = 250
        self.score_update = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.score = 0
        self.isDead = False

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.shoot_delay = 250
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.isDead = False
        
        if pygame.time.get_ticks() - self.score_update > 100:
            if not self.isDead:
                self.score_update = pygame.time.get_ticks()
                player.score += 10
 

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
            self.left = True
            self.right = False

        elif keystate[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.velocity
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.fly_count = 0

        if self.fly_count + 1 > 18:
            self.fly_count = 17

        if self.fly_count - 1 < -18:
            self.fly_count = -17

        if self.left and self.fly_count <= 0:
            self.image = player_anim['left'][abs(self.fly_count) // 3]
            self.fly_count -= 1
        elif self.left and self.fly_count > 0:
            self.image = player_anim['right'][self.fly_count // 3]
            self.fly_count -= 1
        elif self.right and self.fly_count >= 0:
            self.image = player_anim['right'][self.fly_count // 3]
            self.fly_count += 1
        elif self.right and self.fly_count < 0:
            self.image = player_anim['left'][abs(self.fly_count) // 3]
            self.fly_count += 1
        else:
            self.image = player_img


    def hide(self):
        # hide the player when dead
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH + 500, HEIGHT + 200)

    def dead(self, hit):
        self.isDead = True
        self.player_death_expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(self.player_death_expl)
        player.hide()
        player.lives -= 1
        player.health = 100
        

    def isHit(self, hit):
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        player.health -= 35
        
           


# Asteroid class


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        self.image = asteroid_img
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-20, 0)
        self.x_velocity = random.randrange(-1, 1)
        self.radius = 20
       
        self.image.set_colorkey(BLACK)
        self.firerate = 5
        self.y_velocity = random.randrange(2, 4)


    def update(self):
        self.rect.y += self.y_velocity
        self.rect.x += self.x_velocity
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-20, 0)
            self.x_velocity = range_with_no_number(-1, 2, 0)



# Explosion class


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load images
background = pygame.image.load(path.join(img_dir, 'spacebg.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 's0.png')).convert()
player_img.set_colorkey(BLACK)
mini_player_img = pygame.transform.scale(player_img, (25, 25))
asteroid_img = pygame.image.load(
    path.join(img_dir, 'asteroid.png')).convert() 

# Load player animation
player_anim = {'left': [],
               'right': []
               }
for i in range(6):
    filename = 'l{}.png'.format(i)
    img_left = pygame.image.load(path.join(img_dir, filename)).convert()
    img_left.set_colorkey(BLACK)
    player_anim['left'].append(img_left)
    filename = 'r{}.png'.format(i)
    img_right = pygame.image.load(path.join(img_dir, filename)).convert()
    img_right.set_colorkey(BLACK)
    player_anim['right'].append(img_right)


# Load explosion animation
explosion_anim = {'lg': [],
                  'sm': []}
for i in range(6):
    filename = 'e{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale((img), (42, 42))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale((img), (20, 20))
    explosion_anim['sm'].append(img_sm)


# Load sounds
player_exp_sound = pygame.mixer.Sound(path.join(sound_dir, 'player_exp.wav'))
player_exp_sound.set_volume(0.2)

background_sound = pygame.mixer.music.load(path.join(sound_dir, 'theme.ogg'))
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(loops=-1)



            
def main():
    show_start_screen()
    initialise_game()
    game_over = False
    running = True
    # Loop
    while running:
        if game_over:
            show_game_over_screen()
            game_over = False
            initialise_game()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Update sprites
        all_sprites.update()

        # check if the player collides with an asteroid
        hits = pygame.sprite.spritecollide(
            player, asteroids, True, pygame.sprite.collide_circle)
        for hit in hits:
            player_exp_sound.play()
            player.isHit(hit)
            if player.health <= 0:
                player.dead(hit)
            spawn_asteroid_enemy()


        if player.lives < 1 and not player.player_death_expl.alive():
            game_over = True

        # Render
        window.fill(BLACK)
        window.blit(background, background_rect)
        all_sprites.draw(window)
        draw_text(window, str(player.score), 22, WIDTH / 2, 10)
        draw_health_bar(window, WIDTH-205, 5, player.health)
        draw_lives(window, WIDTH-205, 40, player.lives, mini_player_img)
        pygame.display.flip()

    pygame.quit()
    quit()

main()