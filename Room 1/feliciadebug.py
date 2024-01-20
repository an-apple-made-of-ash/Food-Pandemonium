import pygame
import pytmx
import random
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        self.img = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img, (30, 30)) for img in self.img]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_power = 30
        self.gravity = 3
        self.jump = 1
        self.is_jumping = False

    def move(self, keys, obstacles):
        new_position = self.rect.copy()

        # Horizontal Movement
        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            new_position.x -= self.speed
            self.index = 2
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            new_position.x += self.speed
            self.index = 3

        self.image = self.images[self.index]

        # Check for collisions in the horizontal direction
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # Jumping
        if keys[pygame.K_SPACE] and self.jump == 1:
            self.jump -= 1
            if self.jump < 0:
                self.jump = 0
            self.is_jumping = True
            new_position.y -= self.jump_power
            self.is_jumping = False

        if not self.is_jumping:
            new_position.y += self.gravity

        if any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.jump = 1

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

def load_pygame(filename):
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    return tmx_data

def draw_map(surface, tmx_data):
    bg = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'Assets', 'concrete floor.png'))
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Correct the order of arguments in the blit function
                    surface.blit(bg, (x * tmx_data.tilewidth, y * tmx_data.tileheight))
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))


def get_collision_objects(tmx_data, layer_name):
    obstacles = []
    layer = tmx_data.get_layer_by_name("Tile Layer 1")
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    path = os.path.join(os.path.dirname(__file__), 'room1_walls_test.tmx')
    tmx_data = load_pygame(path)
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

    # Path to Assets
    asset_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
    imgs = []
    paths = ["Delivery-Front.png", "Delivery-Back.png", "Delivery-Left.png", "Delivery-Right.png"]
    sprites = [os.path.join(asset_path, path) for path in paths]
    for path in paths: 
        sprite_path = os.path.join(asset_path, path)
        sprites.append(sprite_path)

    # Player setup
    player = Player(100, 100, sprites)  # Width and height set to 40 pixels

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)  # Limit to 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player.move(keys, obstacles)

        screen.fill((0, 0, 0))  # Clear screen
        draw_map(screen, tmx_data)

        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
