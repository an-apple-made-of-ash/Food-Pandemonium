import os
import pygame
from pygame.locals import *
from tiles import *
from collide import *
import random

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position):
        super().__init__()
        self.imag = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img, (38, 38)) for img in self.imag]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 1

    def move(self, obstacles):
        new_position = self.rect.copy()
        keys = pygame.key.get_pressed()
        # Horizontal Movement
        if keys[K_a] or keys[K_LEFT]:
            if not westW:
                new_position.x -= self.speed
                self.index = 2
        if keys[K_d] or keys[K_RIGHT]:
            if not eastW:
                new_position.x += self.speed
                self.index = 3
        if keys[K_w] or keys[K_UP]:
            if not northW:
                new_position.y -= self.speed
                self.index = 1
        if keys[K_s] or keys[K_DOWN]:
            if not southW: 
                new_position.y += self.speed
                self.index = 0

        self.image = self.images[self.index]

        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target_rect):
        return target_rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + self.width // 2
        y = -target.rect.y + self.height // 2

        # Limit camera scroll to map boundaries
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.map_width - self.width), x)  # right
        y = max(-(self.map_height - self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)

# Wind Class
class Wind(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position, direction):
        super().__init__()
        # Select a random path from the list
        image_path = random.choice(image_paths)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 5
        self.direction = direction
    def update(self):
        if self.direction == "North":
            self.rect.y -= self.speed
        elif self.direction == "South":
            self.rect.y += self.speed
        elif self.direction == "West":
            self.rect.x -= self.speed
        elif self.direction == "East":
            self.rect.x += self.speed
pygame.init()



width = 800
height = 600
screen = pygame.display.set_mode([width, height])
path = os.path.join(os.path.dirname(__file__), 'Room 2.tmx')
tmx_data = load_pygame(path)
obstacles = get_collision_objects(tmx_data, "Tile Layer 2")

pygame.display.set_caption("Room 2")
assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
paths = ["Delivery-Front.png", "Delivery-Back.png", "Delivery-Left.png", "Delivery-Right.png"]
sprites = [os.path.join(assets_path, path) for path in paths]

player = Player(sprites, (60, 525))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
camera = Camera(width, height, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

clock = pygame.time.Clock()
move = True
running = True
last_weather_change = 0
eastW = False
westW = False
northW = False
southW = False

rain_path = "C:\\Users\\Couga\\Documents\\GitHub\\hmmmmm\\Assets\\Rain Filter.png"
rain_filter = pygame.image.load(rain_path)

wind_paths = ["C:\\Users\\Couga\\Documents\\GitHub\\hmmmmm\\Assets\\Wind.png",  # Add more paths if needed
              "C:\\Users\\Couga\\Documents\\GitHub\\hmmmmm\\Assets\\Wind.png",
              "C:\\Users\\Couga\\Documents\\GitHub\\hmmmmm\\Assets\\Wind.png"]

winds = []  # List to hold instances of Wind class
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if move:
        player.move(obstacles)
        if current_time - last_weather_change > 5000:
            weather = random.randint(1, 2)
            eastW = False
            westW = False
            northW = False
            southW = False
            player.speed = 1

            if weather == 1:
                wind_direction = random.choice(["North", "South", "East", "West"])
                print(wind_direction + " wind is blowing!")
                if wind_direction != "None":
                    wind = Wind(wind_paths,
                                (random.randint(0, width), random.randint(0, height)),
                                wind_direction)
                    winds.append(wind)
                    all_sprites.add(wind)

            elif weather == 2:
                player.speed = 20
                print("It's Raining")

            last_weather_change = current_time

    all_sprites.update()
    camera.update(player)

    screen.fill((40, 40, 50))
    draw_map(screen, tmx_data, camera)

    if (player.rect.x + player.rect.width) >= 1560 and (player.rect.y + player.rect.height) >= 560:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Dash may have braved the weather but more awaits him...', True, (0, 200, 0))
        textRect = text.get_rect()
        textRect.center = (400, 300)
        screen.fill((255, 255, 255))
        player.rect.topleft = (800, 600)
        screen.blit(text, textRect)
        move = False

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    pygame.display.flip()
    pygame.display.update()

pygame.quit()