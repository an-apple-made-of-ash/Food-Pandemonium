import pygame
import pytmx
import subprocess
from random import shuffle
import os
from tiles import *

pygame.font.init()
import time

passwords = {1: 'hyefxt', 2: 'rwvnxz', 3: 'ctwldx', 4: 'lbimco', 5: 'mactuy', 6: 'fydaea'}
order = [1, 2, 3, 4, 5, 6]
shuffle(order)


def show_popup_text(window, message, duration, pos, font_size=36, color=(255, 255, 255), bgcolor=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(message, True, color, bgcolor)
    window.blit(text_surface, pos)
    pygame.display.update()
    time.sleep(duration)
    window.fill(bgcolor, (pos[0], pos[1], text_surface.get_width(), text_surface.get_height()))
    pygame.display.update()


def load_pygame(filename):
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    return tmx_data


def draw_map(surface, tmx_data):
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))


def get_collision_objects(tmx_data, layer_name):
    obstacles = []
    layer = tmx_data.get_layer_by_name(layer_name)
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        super().__init__()
        self.img = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img, (30, 30)) for img in self.img]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def move(self, keys, border, window):
        new_position = self.rect.copy()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_position.y -= self.speed
            self.index = 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_position.y += self.speed
            self.index = 0
        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            new_position.x += self.speed
            self.index = 3
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            new_position.x -= self.speed
            self.index = 2

        self.image = self.images[self.index]

        # Check for collisions
        if not any(new_position.colliderect(obstacle) for obstacle in border):
            self.rect.topleft = new_position.topleft

def display_answer(order, passwords, player_rect, window):
    for i in range(6):
        if player_rect.colliderect(portal_rects[i]):
            message = f"{order[i]}: {passwords[order[i]]}"
            show_popup_text(window, message, 3, (400, 200))
            return

map = TileMap('treasure_chest_map.csv', "Dark Brick1.png")
screen = pygame.display.set_mode([800, 600])
canvas = pygame.Surface([800, 1200])
path = os.path.join(os.path.dirname(__file__), 'treasure_chest_map.tmx')
tmx_data = load_pygame(path)
border = get_collision_objects(tmx_data, "Border")

# Define the portal rectangles
portal_rects = [
    pygame.Rect(580, 380, 80, 80),
    pygame.Rect(380, 380, 80, 80),
    pygame.Rect(180, 180, 80, 80),
    pygame.Rect(580, 180, 80, 80),
    pygame.Rect(380, 180, 80, 80),
    pygame.Rect(180, 180, 80, 80)
]

pygame.display.set_caption("Room 4")

#Path to Assets
asset_path = "C:/Users/ashle/Documents/ash/hmmmmm/Assets"
imgs = [] 
paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
sprites = []
for path in paths: 
    sprite_path = os.path.join(asset_path, path)
    sprites.append(sprite_path)
# Player setup
player = Player(100, 100, sprites)  # Width and height set to 40 pixels

#Create sprite group and add player to it 
all_sprites = pygame.sprite.Group() 
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move(pygame.key.get_pressed(), border, screen)
    canvas.fill((80, 80, 80))
    map.draw_map(canvas)
    display_answer(order, passwords, player.rect, screen)  # Check for displaying answers
    all_sprites.draw(canvas)
    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    pygame.display.update()

pygame.quit()