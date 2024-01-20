import os
import pygame
from pygame.locals import *
import pytmx
from pytmx import load_pygame


#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position):
        super(Player,self).__init__()
        self.images = [pygame.image.load(path) for path in image_paths]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

    def update(self): 
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.index=2
            self.rect.x -= 5
        if keys[K_RIGHT] or keys[K_d]:
            self.index=3
            self.rect.x += 5
        if keys[K_UP] or keys[K_w]:
            self.index=1
            self.rect.y -= 5
        if keys[K_DOWN] or keys[K_s]:
            self.index=0
            self.rect.y += 5

        self.image = self.images[self.index]
pygame.init() 

screen = pygame.display.set_mode([800,600])
pygame.display.set_caption("Room 4")

#For Sprites 
assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
sprites = []
for path in paths: 
    sprite_path = os.path.join(assets_path, path)
    sprites.append(sprite_path)

player = Player(sprites,(100,100))

#Create sprite group and add player to it 
all_sprites = pygame.sprite.Group() 
all_sprites.add(player)


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
    layer = tmx_data.get_layer_by_name("Border_layer")
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tmx_data = load_pygame(os.path.join(os.path.dirname(__file__),'border.tmx'))
    obstacles = get_collision_objects(tmx_data, "Border_layer")

    # Player setup
    player = pygame.Rect(100, 100, 32, 32)  # Example player rect
    speed = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_position = player.copy()
        if keys[pygame.K_LEFT]:
            new_position.x -= speed
        if keys[pygame.K_RIGHT]:
            new_position.x += speed
        if keys[pygame.K_UP]:
            new_position.y -= speed
        if keys[pygame.K_DOWN]:
            new_position.y += speed

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            player = new_position

        screen.fill((0, 0, 0))  # Clear screen
        draw_map(screen, tmx_data)  
        pygame.draw.rect(screen, (255, 0, 0), player)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
